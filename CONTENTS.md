
[comment]: # (DO NOT EDIT; GENERATED FILE)

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
        - 2017
    * FISHING_MMSI
        * [KNOWN](#link-3)
            - ALL_YEARS
        * KNOWN_AND_LIKELY
            - 2012
            - 2013
            - 2014
            - 2015
            - 2016
            - 2017
            - ANY_YEAR
        * KNOWN_LIKELY_AND_SUSPECTED
            - ANY_YEAR
        * [LIKELY](#link-6)
            - 2012
            - 2013
            - 2014
            - 2015
            - 2016
            - 2017
        * SUSPECTED
            - ANY_YEAR
    * NONFISHING_MMSI
        * [KNOWN](#link-9)
            - ALL_YEARS
    * [SPOOFING_MMSI](#link-10)
        - 2012
        - 2013
        - 2014
        - 2015
        - 2016
        - 2017
    * [VESSEL_INFO](#link-11)
        - CONSOLIDATED_LISTS
        - REEFERS
        * [VESSEL_LISTS](#link-12)
            - ALL_YEARS
            - ATTRIBUTES_2017_12_24
            - ATTRIBUTES_2017_5_18
            - ATTRIBUTES_2017_6_30
            - ATTRIBUTES_2017_7_1
            - ATTRIBUTES_2017_7_10
            - ATTRIBUTES_2017_7_2
            - FISHING_LABELS_2012
            - FISHING_LABELS_2013
            - FISHING_LABELS_2014
            - FISHING_LABELS_2015
            - FISHING_LABELS_2016
            - FISHING_LABELS_2017
            - LABELS_2012
            - LABELS_2013
            - LABELS_2014
            - LABELS_2015
            - LABELS_2016
            - LABELS_2017
            - LABELS_2017_12_24
            - LABELS_2017_5_18
            - LABELS_2017_6_30
            - LABELS_2017_7_1
            - LABELS_2017_7_10
            - LABELS_2017_7_2

---------
## READMEs

<a name="link-1"></a>
### GFW/ACTIVE_MMSI [[toc]](#contents)

[comment]: # (DO NOT EDIT; GENERATED FILE)

#### Active MMSI

*query-version: 2* 

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

<a name="link-3"></a>
### GFW/FISHING_MMSI/KNOWN [[toc]](#contents)

Known fishing vessels derived from GFW/VESSEL_INFO/CONSOLIDATED_LISTS.csv.

--------

<a name="link-6"></a>
### GFW/FISHING_MMSI/LIKELY [[toc]](#contents)

[comment]: # (DO NOT EDIT; GENERATED FILE)

#### Likely Fishing MMSIs 

*query-version: 3*

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
        type in (5, 19, 24)
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

<a name="link-9"></a>
### GFW/NONFISHING_MMSI/KNOWN [[toc]](#contents)

Known non-fishing vessels derived from GFW/VESSEL_INFO/CONSOLIDATED_LISTS.csv.

--------

<a name="link-10"></a>
### GFW/SPOOFING_MMSI [[toc]](#contents)

[comment]: # (DO NOT EDIT; GENERATED FILE)

#### Spoofing MMSI 

*query-version: 3*

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

<a name="link-11"></a>
### GFW/VESSEL_INFO [[toc]](#contents)

CONSOLIDATED_LISTS.csv
======================

Derived from a combination of various registry lists. Combining
code currently lives in `mussidae`.

Fields:

1. mmsi: MMSI
2. label: type of vessel
3. length: meters
4. engine_power: kilowatts
5: tonnage: gross metric tons
6. split: 'Training' | 'Test' (for CNN classifier)


REEFERS.csv
===========

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

--------

<a name="link-12"></a>
### GFW/VESSEL_INFO/VESSEL_LISTS [[toc]](#contents)

Vessel lists generated by the neural net go here
