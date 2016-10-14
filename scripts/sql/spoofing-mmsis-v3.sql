select mmsi from
(
SELECT
  a.mmsi AS mmsi,
  active_days,
  message_count,
  total_days,
  segment_count,
  segment_days,
  segment_days / LEAST(total_days, float(active_days)) AS spoof_ratio,
  segment_days - LEAST(total_days, float(active_days)) AS overlap_days,
  (segment_days - LEAST(total_days, float(active_days))) / LEAST(total_days, float(active_days)) AS spoof_percent,
  (segment_days / LEAST(total_days, float(active_days))) * (segment_days - LEAST(total_days, float(active_days))) as spoof_factor
FROM (
  SELECT
    mmsi,
    COUNT(*) AS active_days,
    SUM(message_count) AS message_count,
    (MAX(max_timestamp) - MIN(min_timestamp)) / 86400 AS total_days
  FROM (
    SELECT
      mmsi,
      UTC_USEC_TO_DAY(timestamp) AS day,
      COUNT(*) message_count,
      MIN(TIMESTAMP_TO_SEC(timestamp)) AS min_timestamp,
      MAX(TIMESTAMP_TO_SEC(timestamp)) AS max_timestamp
    FROM (TABLE_DATE_RANGE([{classify_table_name}.], TIMESTAMP('{start_date}'), TIMESTAMP('{end_date}')))
    WHERE
      RIGHT(seg_id, 3) != 'BAD'
    GROUP BY
      mmsi,
      day )
  GROUP BY
    mmsi ) a
JOIN (
  SELECT
    mmsi,
    COUNT(*) segment_count,
    SUM(max_timestamp - min_timestamp) / 86400 AS segment_days
  FROM (
    SELECT
      mmsi,
      COUNT(*) AS message_count,
      MIN(TIMESTAMP_TO_SEC(timestamp)) AS min_timestamp,
      MAX(TIMESTAMP_TO_SEC(timestamp)) AS max_timestamp
    FROM (TABLE_DATE_RANGE([{classify_table_name}.], TIMESTAMP('{start_date}'), TIMESTAMP('{end_date}')))
    WHERE
      RIGHT(seg_id, 3) != 'BAD'
    GROUP BY
      mmsi,
      seg_id )
  GROUP BY
    mmsi ) b
ON
  a.mmsi = b.mmsi
)
where active_days > 3 and spoof_percent > 0.01