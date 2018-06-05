/* 

# Active MMSI

*query-version: 2* 

MMSIs of vessels which are broadcasting during the specified period.  Only
MMSIs with a minimum number of positional reports are included.

## Query:
*/
SELECT
  mmsi
FROM
(
  SELECT
    mmsi, count(*) as c_pos
  FROM (TABLE_DATE_RANGE([{classify_table_name}], TIMESTAMP('{start_date}'), TIMESTAMP('{end_date}')))
  WHERE
    lat IS NOT NULL AND lon IS NOT NULL
    AND speed > .1 
    AND data_source IS NULL
  GROUP BY
    mmsi
  HAVING
    c_pos > 500
)
