 #StandardSql
 SELECT mmsi, vessel_id FROM (
  SELECT 
    ssvid as mmsi, 
    vessel_id, 
    SUM(pos_count) as pos_count,
    RANK() OVER (PARTITION BY ssvid ORDER BY SUM(pos_count) DESC) as rn 
    FROM `{segment_identity_table}*` 
  GROUP BY ssvid, vessel_id
  ) 
  -- 500 positions is the cutoff for an "active mmsi", so we include all
  -- `vessel_ids` with over 500 positions. We always include at least
  -- one (with the highest count) vessel ID, however.
  WHERE rn = 1 OR pos_count > 500