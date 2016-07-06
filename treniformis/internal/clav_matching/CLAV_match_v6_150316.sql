SELECT
  *
FROM (
  SELECT
    a.mmsi AS mmsi,
    b.shipname AS shipname,
    b.imo AS imo,
    b.callsign AS callsign,
    a.shiptype AS shiptype,
    a.shiptype_fishing AS shiptype_fishing,
    b.clav_TUVI AS clav_TUVI,
    a.rank_imo AS imo_rank,
    a.rank_callsign AS callsign_rank,
    a.rank_name AS name_rank,
    a.flag_match AS flag_match,
    a.date_range_match AS date_range_match,
    a.clav_date_match AS clav_date_match,
    a.fishing_msg_ratio AS fishing_msg_ratio,
    STRING(b.clav_DateUpdated) AS clav_DateUpdated,
    b.rfmo_name AS rfmo_name,
    a.match_start AS match_start,
    a.match_end AS match_end,
    a.match_score AS match_score
  FROM (
    SELECT
      clav_VRMFID,
      mmsi,
      rank_imo,
      rank_callsign,
      rank_name,
      flag_match,
      date_range_match,
      clav_date_match,
      fishing_msg_ratio,
      STRING(match_start) AS match_start,
      STRING(match_end) AS match_end,
      match_score,
      rank_score,
      shiptype,
      shiptype_fishing
    FROM (
      SELECT
        *,
        RANK(match_score) OVER (PARTITION BY clav_VRMFID ORDER BY msg_score DESC) AS rank_score
      FROM (
        SELECT
          *,
          CASE WHEN clav_DateUpdated < match_start
          OR clav_DateUpdated > match_end THEN msg_score2/4 WHEN (fishing_msg_ratio < .1
            AND shiptype_fishing = 1) THEN msg_score2/4 WHEN (flag_match = 0
            AND (rank_imo !=0
              OR rank_callsign != 0)) THEN msg_score2 WHEN (flag_match =1
            AND date_range_match = 0) THEN msg_score2*2 WHEN (flag_match = 1
            AND date_range_match = 1) THEN msg_score2*4 ELSE msg_score2 END AS match_score,
          IF ((clav_DateUpdated > match_start
              AND clav_DateUpdated < match_end), 1, 0) AS clav_date_match
        FROM (
          SELECT
            *,
            CASE WHEN (rank_imo = 0
              AND rank_callsign = 0
              AND flag_match = 0) THEN 0 WHEN (rank_imo = 0
              AND rank_callsign = 0
              AND flag_match =1
              AND shiptype_fishing = 1
              AND fishing_msg_ratio IS NULL) THEN 0 WHEN(rank_imo = 0
              AND rank_name = 0
              AND flag_match =1
              AND shiptype_fishing = 1
              AND fishing_msg_ratio IS NULL) THEN 0 ELSE msg_score END AS msg_score2 FROM (
            SELECT
              *,
              SUM(imo_msg_count+callsign_msg_count+name_msg_count/10) AS msg_score
            FROM (
              SELECT
                a.clav_VRMFID AS clav_VRMFID,
                a.mmsi AS mmsi,
                a.rank_imo AS rank_imo,
                a.rank_callsign AS rank_callsign,
                a.rank_name AS rank_name,
                a.imo_msg_count AS imo_msg_count,
                a.callsign_msg_count AS callsign_msg_count,
                a.name_msg_count AS name_msg_count,
                a.imo_start AS imo_start,
                a.imo_end AS imo_end,
                a.callsign_start AS callsign_start,
                a.callsign_end AS callsign_end,
                a.name_start AS name_start,
                a.name_end AS name_end,
                a.MID_code AS MID_code,
                a.flagcode AS flagcode,
                a.MID_flagcode AS MID_flagcode,
                a.clav_DateUpdated AS clav_DateUpdated,
                a.clav_DateAutStart AS clav_DateAutStart,
                a.clav_DateAutEnd AS clav_DateAutEnd,
                a.match_start AS match_start,
                a.match_end AS match_end,
                a.flag_match AS flag_match,
                a.date_range_match AS date_range_match,
                b.fishing_msg_ratio AS fishing_msg_ratio,
                a.shiptype AS shiptype,
                a.shiptype_fishing AS shiptype_fishing
              FROM (
                SELECT
                  *,
                  CASE WHEN imo_start IS NOT NULL
                  AND callsign_start IS NOT NULL
                  AND name_start IS NOT NULL
                  AND DATEDIFF(imo_start,CURRENT_TIMESTAMP()) <= DATEDIFF(callsign_start,CURRENT_TIMESTAMP())
                  AND DATEDIFF(imo_start,CURRENT_TIMESTAMP()) <= DATEDIFF(name_start,CURRENT_TIMESTAMP()) THEN imo_start WHEN imo_start IS NOT NULL
                  AND callsign_start IS NOT NULL
                  AND name_start IS NOT NULL
                  AND DATEDIFF(callsign_start,CURRENT_TIMESTAMP()) <= DATEDIFF(imo_start,CURRENT_TIMESTAMP())
                  AND DATEDIFF(callsign_start,CURRENT_TIMESTAMP()) <= DATEDIFF(name_start,CURRENT_TIMESTAMP()) THEN callsign_start WHEN imo_start IS NOT NULL
                  AND callsign_start IS NOT NULL
                  AND name_start IS NOT NULL
                  AND DATEDIFF(name_start,CURRENT_TIMESTAMP()) <= DATEDIFF(callsign_start,CURRENT_TIMESTAMP())
                  AND DATEDIFF(name_start,CURRENT_TIMESTAMP()) <= DATEDIFF(imo_start,CURRENT_TIMESTAMP()) THEN name_start WHEN imo_start IS NULL
                  AND callsign_start IS NOT NULL
                  AND name_start IS NOT NULL
                  AND DATEDIFF(callsign_start,CURRENT_TIMESTAMP()) <= DATEDIFF(name_start, CURRENT_TIMESTAMP()) THEN callsign_start WHEN imo_start IS NULL
                  AND callsign_start IS NOT NULL
                  AND name_start IS NOT NULL
                  AND DATEDIFF(name_start,CURRENT_TIMESTAMP()) <= DATEDIFF(callsign_start, CURRENT_TIMESTAMP()) THEN name_start WHEN callsign_start IS NULL
                  AND imo_start IS NOT NULL
                  AND name_start IS NOT NULL
                  AND DATEDIFF(imo_start,CURRENT_TIMESTAMP()) <= DATEDIFF(name_start, CURRENT_TIMESTAMP()) THEN imo_start WHEN callsign_start IS NULL
                  AND imo_start IS NOT NULL
                  AND name_start IS NOT NULL
                  AND DATEDIFF(name_start,CURRENT_TIMESTAMP()) <= DATEDIFF(imo_start, CURRENT_TIMESTAMP()) THEN name_start WHEN name_start IS NULL
                  AND imo_start IS NOT NULL
                  AND callsign_start IS NOT NULL
                  AND DATEDIFF(callsign_start,CURRENT_TIMESTAMP()) <= DATEDIFF(imo_start, CURRENT_TIMESTAMP()) THEN callsign_start WHEN name_start IS NULL
                  AND imo_start IS NOT NULL
                  AND callsign_start IS NOT NULL
                  AND DATEDIFF(imo_start,CURRENT_TIMESTAMP()) <= DATEDIFF(callsign_start, CURRENT_TIMESTAMP()) THEN imo_start WHEN imo_start IS NULL
                  AND callsign_start IS NULL THEN name_start WHEN name_start IS NULL
                  AND imo_start IS NULL THEN callsign_start WHEN name_start IS NULL
                  AND callsign_start IS NULL THEN imo_start END AS match_start,
                  CASE WHEN imo_end IS NOT NULL
                  AND callsign_end IS NOT NULL
                  AND name_end IS NOT NULL
                  AND DATEDIFF(imo_end,CURRENT_TIMESTAMP()) >= DATEDIFF(callsign_end,CURRENT_TIMESTAMP())
                  AND DATEDIFF(imo_end,CURRENT_TIMESTAMP()) >= DATEDIFF(name_end,CURRENT_TIMESTAMP()) THEN imo_end WHEN imo_end IS NOT NULL
                  AND callsign_end IS NOT NULL
                  AND name_end IS NOT NULL
                  AND DATEDIFF(callsign_end,CURRENT_TIMESTAMP()) >= DATEDIFF(imo_end,CURRENT_TIMESTAMP())
                  AND DATEDIFF(callsign_end,CURRENT_TIMESTAMP()) >= DATEDIFF(name_end,CURRENT_TIMESTAMP()) THEN callsign_end WHEN imo_end IS NOT NULL
                  AND callsign_end IS NOT NULL
                  AND name_end IS NOT NULL
                  AND DATEDIFF(name_end,CURRENT_TIMESTAMP()) >= DATEDIFF(callsign_end,CURRENT_TIMESTAMP())
                  AND DATEDIFF(name_end,CURRENT_TIMESTAMP()) >= DATEDIFF(imo_end,CURRENT_TIMESTAMP()) THEN name_end WHEN imo_end IS NULL
                  AND callsign_end IS NOT NULL
                  AND name_end IS NOT NULL
                  AND DATEDIFF(callsign_end,CURRENT_TIMESTAMP()) >= DATEDIFF(name_end, CURRENT_TIMESTAMP()) THEN callsign_end WHEN imo_end IS NULL
                  AND callsign_end IS NOT NULL
                  AND name_end IS NOT NULL
                  AND DATEDIFF(name_end,CURRENT_TIMESTAMP()) >= DATEDIFF(callsign_end, CURRENT_TIMESTAMP()) THEN name_end WHEN callsign_end IS NULL
                  AND imo_end IS NOT NULL
                  AND name_end IS NOT NULL
                  AND DATEDIFF(imo_end,CURRENT_TIMESTAMP()) >= DATEDIFF(name_end, CURRENT_TIMESTAMP()) THEN imo_end WHEN callsign_end IS NULL
                  AND imo_end IS NOT NULL
                  AND name_end IS NOT NULL
                  AND DATEDIFF(name_end,CURRENT_TIMESTAMP()) >= DATEDIFF(imo_end, CURRENT_TIMESTAMP()) THEN name_end WHEN name_end IS NULL
                  AND imo_end IS NOT NULL
                  AND callsign_end IS NOT NULL
                  AND DATEDIFF(callsign_end,CURRENT_TIMESTAMP()) >= DATEDIFF(imo_end, CURRENT_TIMESTAMP()) THEN callsign_end WHEN name_end IS NULL
                  AND imo_end IS NOT NULL
                  AND callsign_end IS NOT NULL
                  AND DATEDIFF(imo_end,CURRENT_TIMESTAMP()) >= DATEDIFF(callsign_end, CURRENT_TIMESTAMP()) THEN imo_end WHEN imo_end IS NULL
                  AND callsign_end IS NULL THEN name_end WHEN name_end IS NULL
                  AND imo_end IS NULL THEN callsign_end WHEN name_end IS NULL
                  AND callsign_end IS NULL THEN imo_end END AS match_end,
                  CASE WHEN flagcode = mid_flagcode THEN 1 ELSE 0 END AS flag_match,
                  //flag match
                  CASE WHEN ((DATEDIFF(imo_start, callsign_start) < 10
                      AND DATEDIFF(imo_start, name_start) < 10
                      AND DATEDIFF(callsign_start, name_start) < 10
                      AND DATEDIFF(imo_end, callsign_end) < 10
                      AND DATEDIFF(imo_end, name_end) < 10
                      AND DATEDIFF(callsign_end, name_end) < 10 )
                    OR ( imo_start IS NULL
                      AND DATEDIFF(callsign_start, name_start) < 10
                      AND DATEDIFF(callsign_end, name_end) < 10)
                    OR (callsign_start IS NULL
                      AND DATEDIFF(imo_start, name_start) < 10
                      AND DATEDIFF(imo_end, name_end) < 10)
                    OR (name_start IS NULL
                      AND DATEDIFF(imo_start, callsign_start) < 10
                      AND DATEDIFF(imo_end, callsign_end) < 10) ) THEN 1 ELSE 0 END AS date_range_match,
                  //date match within 10 days
                  IF(shiptype IN ('Fish carriers',
                      'Support Vessels',
                      'Non-fishing vessels nei',
                      'Bunkers',
                      'Fishery research vessels',
                      'Motherships',
                      'Tuna motherships',
                      'Motherships nei'),0,1) AS shiptype_fishing
                FROM (
                  SELECT
                    a.clav_VRMFID AS clav_VRMFID,
                    a.mmsi AS mmsi,
                    a.rank_imo AS rank_imo,
                    a.rank_callsign AS rank_callsign,
                    a.rank_name AS rank_name,
                    a.imo_msg_count AS imo_msg_count,
                    a.callsign_msg_count AS callsign_msg_count,
                    a.name_msg_count AS name_msg_count,
                    a.imo_start AS imo_start,
                    a.imo_end AS imo_end,
                    a.callsign_start AS callsign_start,
                    a.callsign_end AS callsign_end,
                    a.name_start AS name_start,
                    a.name_end AS name_end,
                    a.MID_code AS MID_code,
                    a.flagcode AS flagcode,
                    a.clav_DateUpdated AS clav_DateUpdated,
                    a.clav_DateAutStart AS clav_DateAutStart,
                    a.clav_DateAutEnd AS clav_DateAutEnd,
                    b.Alpha_3 AS MID_flagcode,
                    a.shiptype AS shiptype
                  FROM (
                    SELECT
                      clav_VRMFID,
                      mmsi,
                      MAX(rank_imo) AS rank_imo,
                      MAX(rank_callsign) AS rank_callsign,
                      MAX(rank_name) AS rank_name,
                      MAX(imo_msg_count) AS imo_msg_count,
                      MAX(callsign_msg_count) AS callsign_msg_count,
                      MAX(name_msg_count) AS name_msg_count,
                      MAX(imo_start) AS imo_start,
                      MAX(imo_end) AS imo_end,
                      MAX(callsign_start) AS callsign_start,
                      MAX(callsign_end) AS callsign_end,
                      MAX(name_start) AS name_start,
                      MAX(name_end) AS name_end,
                      MID_code,
                      flagcode,
                      clav_DateUpdated,
                      clav_DateAutStart,
                      clav_DateAutEnd,
                      shiptype
                    FROM (
                      SELECT
                        clav_VRMFID,
                        mmsi,
                        rank_imo,
                        rank_callsign,
                        rank_name,
                        IFNULL(imo_msg_count,0) AS imo_msg_count,
                        IFNULL(callsign_msg_count,0) AS callsign_msg_count,
                        IFNULL(name_msg_count,0) AS name_msg_count,
                        imo_start,
                        imo_end,
                        callsign_start,
                        callsign_end,
                        name_start,
                        name_end,
                        MID_code,
                        flagcode,
                        clav_DateUpdated,
                        clav_DateAutStart,
                        clav_DateAutEnd,
                        shiptype
                      FROM (
                        SELECT
                          clav_VRMFID,
                          mmsi,
                          RANK(msg_count) OVER (PARTITION BY clav_VRMFID ORDER BY msg_count DESC) AS rank_imo,
                          msg_count AS imo_msg_count,
                          first_timestamp AS imo_start,
                          last_timestamp AS imo_end,
                          LEFT(STRING(mmsi), 3) AS MID_code,
                          flagcode,
                          clav_DateUpdated,
                          clav_DateAutStart,
                          clav_DateAutEnd,
                          shiptype
                        FROM (
                          SELECT
                            a.clav_VRMFID AS clav_VRMFID,
                            a.cons_imo2,
                            b.imo,
                            b.first_timestamp AS first_timestamp,
                            b.last_timestamp AS last_timestamp,
                            b.mmsi AS mmsi,
                            b.msg_count AS msg_count,
                            a.clav_FlagCode AS flagcode,
                            a.clav_DateUpdated AS clav_DateUpdated,
                            a.clav_DateAutStart AS clav_DateAutStart,
                            a.clav_DateAutEnd AS clav_DateAutEnd,
                            a.shiptype AS shiptype
                          FROM (
                            SELECT
                              *
                            FROM
                              [Registry_matching_sources.CLAV_cons_imo2_flag_match_3_15]
                            WHERE
                              cons_imo2 IS NOT NULL) a
                          LEFT JOIN (
                            SELECT
                              mmsi,
                              imo,
                              msg_count,
                              first_timestamp,
                              last_timestamp
                            FROM
                              [Vessel_identity_messages.imo_chk_sum]
                            WHERE
                              imo IN (
                              SELECT
                                cons_imo2
                              FROM
                                [Registry_matching_sources.CLAV_cons_imo2_flag_match_3_15])
                              AND msg_count > 10) b
                          ON
                            a.cons_imo2 = b.imo)                                          // imo match
                        WHERE
                          mmsi IS NOT NULL),
                        (
                        SELECT
                          clav_VRMFID,
                          mmsi,
                          RANK(msg_count) OVER (PARTITION BY clav_VRMFID ORDER BY msg_count DESC) AS rank_callsign,
                          msg_count AS callsign_msg_count,
                          first_timestamp AS callsign_start,
                          last_timestamp AS callsign_end,
                          LEFT(STRING(mmsi), 3) AS MID_code,
                          flagcode,
                          clav_DateUpdated,
                          clav_DateAutStart,
                          clav_DateAutEnd,
                          shiptype
                        FROM (
                          SELECT
                            a.clav_VRMFID AS clav_VRMFID,
                            a.callsign,
                            b.callsign,
                            b.first_timestamp AS first_timestamp,
                            b.last_timestamp AS last_timestamp,
                            b.mmsi AS mmsi,
                            b.msg_count AS msg_count,
                            a.clav_FlagCode AS flagcode,
                            a.clav_DateUpdated AS clav_DateUpdated,
                            a.clav_DateAutStart AS clav_DateAutStart,
                            a.clav_DateAutEnd AS clav_DateAutEnd,
                            a.shiptype AS shiptype
                          FROM (
                            SELECT
                              *
                            FROM
                              [Registry_matching_sources.CLAV_cons_imo2]
                            WHERE
                              callsign IS NOT NULL) a
                          LEFT JOIN (
                            SELECT
                              mmsi,
                              callsign,
                              msg_count,
                              first_timestamp,
                              last_timestamp
                            FROM
                              [Vessel_identity_messages.callsigns_rank_mmsi_cnt]
                            WHERE
                              callsign IN (
                              SELECT
                                callsign
                              FROM
                                [Registry_matching_sources.CLAV_cons_imo2])
                              AND msg_count > 10) b
                          ON
                            a.callsign = b.callsign)                                //callsign match
                        WHERE
                          mmsi IS NOT NULL),
                        (
                        SELECT
                          clav_VRMFID,
                          mmsi,
                          RANK(msg_count) OVER (PARTITION BY clav_VRMFID ORDER BY msg_count DESC) AS rank_name,
                          msg_count AS name_msg_count,
                          first_timestamp AS name_start,
                          last_timestamp AS name_end,
                          LEFT(STRING(mmsi), 3) AS MID_code,
                          flagcode,
                          clav_DateUpdated,
                          clav_DateAutStart,
                          clav_DateAutEnd,
                          shiptype
                        FROM (
                          SELECT
                            a.clav_VRMFID AS clav_VRMFID,
                            a.calc_normshipname,
                            b.normalized_shipname,
                            b.first_timestamp AS first_timestamp,
                            b.last_timestamp AS last_timestamp,
                            b.mmsi AS mmsi,
                            b.msg_count AS msg_count,
                            a.clav_FlagCode AS flagcode,
                            a.clav_DateUpdated AS clav_DateUpdated,
                            a.clav_DateAutStart AS clav_DateAutStart,
                            a.clav_DateAutEnd AS clav_DateAutEnd,
                            a.shiptype AS shiptype
                          FROM (
                            SELECT
                              *
                            FROM
                              [Registry_matching_sources.CLAV_cons_imo2]
                            WHERE
                              calc_normshipname IS NOT NULL) a
                          LEFT JOIN (
                            SELECT
                              mmsi,
                              normalized_shipname,
                              msg_count,
                              first_timestamp,
                              last_timestamp
                            FROM
                              [Vessel_identity_messages.norm_shipname_rank_mmsi_cnt]
                            WHERE
                              normalized_shipname IN (
                              SELECT
                                calc_normshipname
                              FROM
                                [Registry_matching_sources.CLAV_cons_imo2])
                              AND msg_count > 10) b
                          ON
                            a.calc_normshipname = b.normalized_shipname) )                 // Shipname match
                      WHERE
                        mmsi IS NOT NULL)
                    GROUP BY
                      clav_VRMFID,
                      mmsi,
                      MID_code,
                      flagcode,
                      clav_DateUpdated,
                      clav_DateAutStart,
                      clav_DateAutEnd,
                      shiptype
                    ORDER BY
                      clav_VRMFID ASC) a
                  LEFT JOIN (
                    SELECT
                      *
                    FROM
                      [scratch_bjorn.MID_code_table]) b
                  ON
                    a.MID_code = b.MID)) a
              LEFT JOIN (
                SELECT
                  mmsi,
                  COUNT(*) c_msg,
                  sum (shiptype_text = 'Fishing') c_fishing,
                  sum (shiptype_text = 'Fishing') / COUNT(*) fishing_msg_ratio
                FROM
                  [Vessel_identity_messages.type5_24_2012_2015]
                WHERE
                  type IN (5,
                    24)
                  AND shiptype_text IS NOT NULL
                  AND shiptype_text != 'Not available'
                  AND timestamp >= '2012-01-01 00:00:00'
                  AND timestamp < '2015-12-01 00:00:00'
                GROUP EACH BY
                  mmsi
                HAVING
                  c_fishing > 10) b
              ON
                a.mmsi = b.mmsi )
            GROUP BY
              clav_VRMFID,
              mmsi,
              rank_imo,
              rank_callsign,
              rank_name,
              imo_msg_count,
              callsign_msg_count,
              name_msg_count,
              imo_start,
              imo_end,
              callsign_start,
              callsign_end,
              name_start,
              name_end,
              MID_code,
              flagcode,
              clav_DateUpdated,
              clav_DateAutStart,
              clav_DateAutEnd,
              MID_flagcode,
              flag_match,
              date_range_match,
              match_start,
              match_end,
              fishing_msg_ratio,
              shiptype,
              shiptype_fishing))))
    WHERE
      rank_score = 1
      AND match_score != 0) a
  LEFT JOIN (
    SELECT
      *
    FROM
      [Registry_matching_sources.CLAV_12_14_2015]) b
  ON
    a.clav_VRMFID = b.clav_VRMFID)
WHERE
  RIGHT(STRING(mmsi), 6) != '000000'
  AND mmsi != 111111111
  AND ((imo_rank != 0
      AND callsign_rank != 0)
    OR (imo_rank !=0
      AND name_rank != 0)
    OR (callsign_rank !=0
      AND name_rank !=0)
    OR (imo_rank !=0
      AND flag_match = 1) )
  AND match_end > '2015-01-31 00:00:00'