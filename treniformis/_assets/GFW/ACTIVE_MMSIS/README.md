Active MMSIs
============

MMSIs of vessels which are broadcasting during the specified period.  Only
MMSIs with a minimum number of positional reports are included.


Migration
---------

Files that were deleted during the migration from `vessel-lists`, but whose
content needs to be preserved.

### active-mmsis-v1.sql ###

```sql
SELECT
  mmsi
FROM
(
  SELECT
    mmsi, count(*) as c_pos
  FROM (TABLE_DATE_RANGE([pipeline_normalize.], TIMESTAMP('{{START_DATE}}'), TIMESTAMP('{{END_DATE}}')))
  WHERE
    lat IS NOT NULL AND lon IS NOT NULL
  GROUP BY
    mmsi
  HAVING
    c_pos > 1000
)
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
QUERY_TEMPLATE=$(cat active-mmsis-v1.sql)

echo "This may take a while, so be patient..."

for RANGE in "${DATE_RANGES[@]}"
do
  read -a DATES <<<"$RANGE"

  QUERY=${QUERY_TEMPLATE//'{{START_DATE}}'/${DATES[0]}}
  QUERY=${QUERY//'{{END_DATE}}'/${DATES[1]}}
  YEAR=${DATES[0]:0:4}
  echo "  ${YEAR}"
  echo ${QUERY} | bq --project=${PROJECT} -q query --format=csv --max_rows 1000000 | tail -n +2 > active-mmsis-${YEAR}-v1.txt
done

echo "Done."
```
