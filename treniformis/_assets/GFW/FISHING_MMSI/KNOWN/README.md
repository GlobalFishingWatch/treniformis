# Known Fishing Vessels Version 1

List of MMSIs that are known to be fishing vessels based on the presence of the MMSI on one or more 
public registries.


Migration
---------

Files that were deleted during the migration from `vessel-lists`, but whose
content needs to be preserved.

### export.sh ###

```bash
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
```

### known-fishing-2014-v1.sql ###

```sql
SELECT
  mmsi
FROM (
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
```

### known-fishing-2015-v1.txt ###

```sql
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
```