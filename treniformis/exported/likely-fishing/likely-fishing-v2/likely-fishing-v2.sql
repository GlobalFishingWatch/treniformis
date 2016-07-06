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
