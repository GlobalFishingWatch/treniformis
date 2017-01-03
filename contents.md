# Treniformis
<a name="contents">
## Contents
</a>
* GFW
    * [ACTIVE_MMSI](#link-1)
        - 2012
        - 2013
        - 2014
        - 2015
        - 2016
    * FINE_LABELS
        - 2012
        - 2013
        - 2014
        - 2015
        - 2016
        - ALL_YEARS
    * FISHING_MMSI
        * [KNOWN](#link-4)
            - 2014
            - 2015
        * KNOWN_AND_LIKELY
            - 2012
            - 2013
            - 2014
            - 2015
            - 2016
        * [LIKELY](#link-6)
            - 2012
            - 2013
            - 2014
            - 2015
            - 2016
    * [SPOOFING_MMSI](#link-7)
        - 2012
        - 2013
        - 2014
        - 2015
        - 2016
    * [VESSEL_INFO](#link-8)
        - REEFERS

---------
## READMEs

<a name="link-1"></a>
### GFW/ACTIVE_MMSI [[toc]](#contents)

#### Active MMSI

*Version: 2* 

MMSIs of vessels which are broadcasting during the specified period.  Only
MMSIs with a minimum number of positional reports are included.

##### Query:
    
    SELECT
      mmsi
    FROM
    (
      SELECT
        mmsi, count(*) as c_pos
      FROM (TABLE_DATE_RANGE([{normalize_table_name}.], TIMESTAMP('{start_date}'), TIMESTAMP('{end_date}')))
      WHERE
        lat IS NOT NULL AND lon IS NOT NULL
         and speed > .1 
      GROUP BY
        mmsi
      HAVING
        c_pos > 500
    )

--------

<a name="link-4"></a>
### GFW/FISHING_MMSI/KNOWN [[toc]](#contents)

version-1
    
    SELECT
      mmsi
    FROM (
      SELECT
        mmsi,
        shipname,
        callsign,
        '' AS imo,
        national_id,
        'ITU' AS source
      FROM
        [Registry_matching_sources.ITU_Dec_2015_Fishing]),
      (
      SELECT
        mmsi,
        shipname,
        callsign,
        '' AS imo,
        Registration_Nbr AS national_id,
        'EU' AS source
      FROM
        [EU_match_results.EU_v2]),
      (
      SELECT
        ffa_mmsi AS mmsi,
        shipname,
        callsign,
        STRING(imo) AS imo,
        national_id,
        'FFA' AS source
      FROM
        [Registry_matching_sources.FFA_11_30_2015]
      WHERE
        ffa_mmsi IS NOT NULL
        AND ffa_VESSEL_TYPE NOT IN ('Bunker',
          'Fish Carrier',
          'Mothership')),
      (
      SELECT
        mmsi,
        shipname,
        callsign,
        STRING(imo) AS imo,
        '' AS national_id,
        'CLAV' AS source
      FROM
        [CLAV_match_results.v7_results]
      WHERE
        shiptype_fishing = 1 ),
      (
      SELECT
        mmsi,
        shipname,
        callsign,
        imo,
        '' AS national_id,
        'CCAMLR' AS source
      FROM
        [Registry_matching_sources.CCAMLR_July_2015_with_mmsi])
      where
        mmsi > 100000
        and mmsi not in (100000000,111111110,111111111,124345678,123456789, 222222222, 999999999) //likely spoofing
        and mmsi not in (987357573,987357579,987357559,986737000,983712160,987357529) // helicopters
        and RIGHT(STRING(mmsi), 6) != '000000' //likely spoofing
    ORDER BY
      mmsi ASC

--------

<a name="link-6"></a>
### GFW/FISHING_MMSI/LIKELY [[toc]](#contents)

#### Likely Fishing MMSIs 

*Version: 3*

MMSIs of vessels which declare the vessel type to be 'Fishing' in type 5 or 24 

Based on this query: https://github.com/GlobalFishingWatch/pleuston/issues/28

See the query committed here for the precise definition.  Basically this is
vessels that have > 1000 positional messages in a year and always declare a 
vessel type of 'Fishing'

##### For Reference

###### Some stuff form Bjorn via slack ###

https://globalfishingwatch.slack.com/files/bjorn/F1F3WFX9S/2015_likely_fishing_list_query.sql

https://globalfishingwatch.slack.com/files/bjorn/F1F2U7F2P/2015_known_fishing.sql

https://globalfishingwatch.slack.com/archives/identity-matching/p1465393952000011


###### Other stuff ###

https://github.com/GlobalFishingWatch/pleuston/issues/27

https://github.com/GlobalFishingWatch/vessel-lists/issues/16

https://github.com/SkyTruth/Benthos/issues/390


###### Google Docs ###

https://docs.google.com/document/d/1QnhgyQ3jtGF83a5-4j25hsvPkh6JNT8vGi8ftWx1UUY/edit

https://docs.google.com/spreadsheets/d/12OVeOxg9N1NViKxH4B7nW31-MwAHW_mS3zPBe2kfIuQ/edit#gid=0

##### Query:
    
    select a.mmsi as mmsi from
    (
      SELECT
        mmsi,
        count(*) c_msg,
        sum (shiptype_text = 'Fishing') c_fishing,
        sum (shiptype_text = 'Fishing') / count(*) fishing_msg_ratio
      FROM (TABLE_DATE_RANGE([{normalize_table_name}.], TIMESTAMP('{start_date}'), TIMESTAMP('{end_date}')))
      WHERE
        type in (5, 24)
        and shiptype_text is not null
        and shiptype_text != 'Not available'
      GROUP EACH BY
        mmsi
      HAVING
        c_fishing > 10 and fishing_msg_ratio > .99
    ) a
    JOIN EACH
    (
      SELECT
        integer(mmsi) as mmsi, COUNT(*) AS c_pos
      FROM (TABLE_DATE_RANGE([{normalize_table_name}.], TIMESTAMP('{start_date}'), TIMESTAMP('{end_date}')))
      WHERE
        lat IS NOT NULL AND lon IS NOT NULL
        and mmsi not in (987357573,987357579,987357559,986737000,983712160,987357529) // helicopters
        and speed > .1
      GROUP BY
        mmsi
      HAVING
        c_pos > 500
    ) b
    ON a.mmsi = b.mmsi

--------

<a name="link-7"></a>
### GFW/SPOOFING_MMSI [[toc]](#contents)

#### Spoofing MMSI 

*Version: 3*

List of MMSIs that experience substantial ID spoofing

By ID spoofing, we mean two or more vessels that are using the same MMSI at the same time. 

All the messages for an MMSI are grouped into sets of tracks that are contiguous spatially and temporally.  
Each continuous track has a unique seg_id field added.  Some tracks contain invalid lan/lon (like 91, 181) and 
are put into a special 'BAD' segment. 

The test for spoofing is fairly naive - we simple compute the extent of each segment in time, add them all up, 
and compare that to the extent of time that the vessel is active.  If the segment time is longer than the 
active time, then we know that some of the segments must overlap, and this is the indication of ID spoofing.

##### Query:
    
    select mmsi from
    (
    SELECT
      a.mmsi AS mmsi,
      active_days,
      message_count,
      total_days,
      segment_count,
      segment_days,
      segment_days / LEAST(total_days, float(active_days)) AS spoof_ratio,
      segment_days - LEAST(total_days, float(active_days)) AS overlap_days,
      (segment_days - LEAST(total_days, float(active_days))) / LEAST(total_days, float(active_days)) AS spoof_percent,
      (segment_days / LEAST(total_days, float(active_days))) * (segment_days - LEAST(total_days, float(active_days))) as spoof_factor
    FROM (
      SELECT
        mmsi,
        COUNT(*) AS active_days,
        SUM(message_count) AS message_count,
        (MAX(max_timestamp) - MIN(min_timestamp)) / 86400 AS total_days
      FROM (
        SELECT
          mmsi,
          UTC_USEC_TO_DAY(timestamp) AS day,
          COUNT(*) message_count,
          MIN(TIMESTAMP_TO_SEC(timestamp)) AS min_timestamp,
          MAX(TIMESTAMP_TO_SEC(timestamp)) AS max_timestamp
        FROM (TABLE_DATE_RANGE([{classify_table_name}.], TIMESTAMP('{start_date}'), TIMESTAMP('{end_date}')))
        WHERE
          RIGHT(seg_id, 3) != 'BAD'
        GROUP BY
          mmsi,
          day )
      GROUP BY
        mmsi ) a
    JOIN (
      SELECT
        mmsi,
        COUNT(*) segment_count,
        SUM(max_timestamp - min_timestamp) / 86400 AS segment_days
      FROM (
        SELECT
          mmsi,
          COUNT(*) AS message_count,
          MIN(TIMESTAMP_TO_SEC(timestamp)) AS min_timestamp,
          MAX(TIMESTAMP_TO_SEC(timestamp)) AS max_timestamp
        FROM (TABLE_DATE_RANGE([{classify_table_name}.], TIMESTAMP('{start_date}'), TIMESTAMP('{end_date}')))
        WHERE
          RIGHT(seg_id, 3) != 'BAD'
        GROUP BY
          mmsi,
          seg_id )
      GROUP BY
        mmsi ) b
    ON
      a.mmsi = b.mmsi
    )
    where active_days > 3 and spoof_percent > 0.01

--------

<a name="link-8"></a>
### GFW/VESSEL_INFO [[toc]](#contents)

#### REEFERS.csv

Fields:

1. mmsi: MMSI
2. imo: IMO (if available)
3. call_sign: vessel callsign
4. width: width of vessel
5. avg_length: average vessel total overall length (LOA) in meters
6. stddev_length: standard deviation of vessel length, meters
7. num_length_sources: number values used to calculate avg and std dev of length
8. avg_gross_tonnage: average vessel gross tonnage
9. stddev_gross_tonnage: standard deviation of gross tonnage (tons)
10. num_gross_tonnage_sources: number of values used to calculate avg and std dev of tonnage
11. dead_weight: vessel deadweight (tons)
12. source: where information from vessel was obtained:

    - CLAV = CLAV registry list (from BQ)
    - ITU = ITU registry list (from BQ)
    - ICCAT = ICCAT registry (Dahlhousie students)
    - WCPFC = Western and Central Pacific Tuna Commision registry
    - FFA = FFA registry (from BQ)
    - CCSBT = CCSBT registries (Dahlhousie students)
    - encounters = vessels identified from encounters, information from MarineTraffic
            
13. flag_state: flag state of vessel (from MID codes)
