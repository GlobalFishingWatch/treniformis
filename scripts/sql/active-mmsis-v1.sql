SELECT
  mmsi
FROM
(
  SELECT
    mmsi, count(*) as c_pos
  FROM (TABLE_DATE_RANGE([{normalize_table_name}.], TIMESTAMP('{start_date}'), TIMESTAMP('{end_date}')))
  WHERE
    lat IS NOT NULL AND lon IS NOT NULL
  GROUP BY
    mmsi
  HAVING
    c_pos > 1000
)
