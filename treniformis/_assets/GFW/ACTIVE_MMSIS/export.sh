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