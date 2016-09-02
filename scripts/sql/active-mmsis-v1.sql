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
