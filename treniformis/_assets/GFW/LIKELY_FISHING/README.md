Likely Fishing MMSIs version 2
==============================

MMSIs of vessels which declare the vessel type to be 'Fishing' in type 5 or 24 

Based on this query: https://github.com/GlobalFishingWatch/pleuston/issues/28

See the query committed here for the precise definition.  Basically this is
vessels that have > 1000 positional messages in a year and always declare a 
vessel type of 'Fishing'

For Reference
-------------

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


Migration
---------

Files that were deleted during the migration from `vessel-lists`, but whose
content needs to be preserved.


### likely-fishing-v2.sql ### 

```sql
select a.mmsi as mmsi from
(
  SELECT
    mmsi,
    count(*) c_msg,
    sum (shiptype_text = 'Fishing') c_fishing,
    sum (shiptype_text = 'Fishing') / count(*) fishing_msg_ratio
  FROM (TABLE_DATE_RANGE([pipeline_normalize.], TIMESTAMP('{{START_DATE}}'), TIMESTAMP('{{END_DATE}}')))
  WHERE
    type in (5, 24)
    and shiptype_text is not null
    and shiptype_text != 'Not available'
  GROUP EACH BY
    mmsi
  HAVING
    c_fishing > 10 and fishing_msg_ratio = 1.0
) a
JOIN EACH
(
  SELECT
    integer(mmsi) as mmsi, COUNT(*) AS c_pos
  FROM (TABLE_DATE_RANGE([pipeline_normalize.], TIMESTAMP('{{START_DATE}}'), TIMESTAMP('{{END_DATE}}')))
  WHERE
    lat IS NOT NULL AND lon IS NOT NULL
  GROUP BY
    mmsi
  HAVING
    c_pos > 1000
)b
ON a.mmsi = b.mmsi
```


### test_query.sql ###

```sql
  SELECT
    mmsi
  FROM (TABLE_DATE_RANGE([pipeline_normalize.], TIMESTAMP('{{START_DATE}}'), TIMESTAMP('{{END_DATE}}')))
  group by mmsi
  limit 100000
```


### export.sh ###

```bash
#!/bin/bash

PROJECT=world-fishing-827


DATE_RANGES=( \
  "2012-01-01 2013-01-01"  \
  "2013-01-01 2014-01-01"  \
  "2014-01-01 2015-01-01"  \
  "2015-01-01 2016-01-01"  \
  "2016-01-01 2016-06-01"  \
)
QUERY_TEMPLATE=$(cat likely-fishing-v2.sql)


#DATE_RANGES=( \
#  "2015-01-01 2016-01-01"  \
#)
#QUERY_TEMPLATE=$(cat test_query.sql)


echo "This may take a while, so be patient..."

for RANGE in "${DATE_RANGES[@]}"
do
  read -a DATES <<<"$RANGE"

  QUERY=${QUERY_TEMPLATE//'{{START_DATE}}'/${DATES[0]}}
  QUERY=${QUERY//'{{END_DATE}}'/${DATES[1]}}
  YEAR=${DATES[0]:0:4}
  echo "  ${YEAR}"
  echo ${QUERY} | bq --project=${PROJECT} -q query --format=csv --max_rows 100000 | tail -n +2 > likely-fishing-${YEAR}-v2.txt
done

echo "Done."
```