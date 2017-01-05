
[comment]: # (DO NOT EDIT; GENERATED FILE)

# Likely Fishing MMSIs 

*Version: 3*

MMSIs of vessels which declare the vessel type to be 'Fishing' in type 5 or 24 

Based on this query: https://github.com/GlobalFishingWatch/pleuston/issues/28

See the query committed here for the precise definition.  Basically this is
vessels that have > 1000 positional messages in a year and always declare a 
vessel type of 'Fishing'

## For Reference

### Some stuff form Bjorn via slack ###

https://globalfishingwatch.slack.com/files/bjorn/F1F3WFX9S/2015_likely_fishing_list_query.sql

https://globalfishingwatch.slack.com/files/bjorn/F1F2U7F2P/2015_known_fishing.sql

https://globalfishingwatch.slack.com/archives/identity-matching/p1465393952000011


### Other stuff ###

https://github.com/GlobalFishingWatch/pleuston/issues/27

https://github.com/GlobalFishingWatch/vessel-lists/issues/16

https://github.com/SkyTruth/Benthos/issues/390


### Google Docs ###

https://docs.google.com/document/d/1QnhgyQ3jtGF83a5-4j25hsvPkh6JNT8vGi8ftWx1UUY/edit

https://docs.google.com/spreadsheets/d/12OVeOxg9N1NViKxH4B7nW31-MwAHW_mS3zPBe2kfIuQ/edit#gid=0

## Query:
    
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