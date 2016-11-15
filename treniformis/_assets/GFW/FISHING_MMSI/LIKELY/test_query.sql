  SELECT
    mmsi
  FROM (TABLE_DATE_RANGE([pipeline_normalize.], TIMESTAMP('{{START_DATE}}'), TIMESTAMP('{{END_DATE}}')))
  group by mmsi
  limit 100000
