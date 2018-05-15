  #standardSQL
  SELECT mmsi, vessel_id FROM (
  SELECT 
    ssvid as mmsi, 
    vessel_id, 
    RANK() OVER (PARTITION BY ssvid ORDER BY SUM(pos_count) DESC) as rn 
    FROM `{segment_identity_table}*` 
  GROUP BY ssvid, vessel_id
  ) WHERE rn = 1