#!/bin/bash

echo "Exporting Known Fishing MMSIs for 2014..."
cat known-fishing-2014-v1.sql \
  | bq --project=world-fishing-827 -q query --format=csv --max_rows 100000 \
  | tail -n +2 \
  > known-fishing-2014-v1.txt

echo "Exporting Known Fishing MMSIs for 2015..."
cat known-fishing-2015-v1.sql \
  | bq --project=world-fishing-827 -q query --format=csv --max_rows 100000 \
  | tail -n +2 \
  > known-fishing-2015-v1.txt

