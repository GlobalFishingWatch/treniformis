SELECT
  *
FROM (
  SELECT
    a.row_number AS row_number,
    a.mmsi AS mmsi,
    b.shipname AS shipname,
    b.callsign AS callsign,
    b.Registration_Nbr AS Registration_Nbr,
    b.Country_Code AS Country_Code,
    b.Gear_Main_Code AS Gear_Main_Code,
    b.Gear_Sec_Code AS Gear_Sec_Code,
    a.rank_callsign AS callsign_rank,
    a.rank_name AS name_rank,
    a.flag_match AS flag_match,
    a.fishing_msg_ratio AS fishing_msg_ratio,
    STRING(a.name_start) AS name_start,
    STRING(a.name_end) AS name_end_end,
    STRING(a.callsign_start) AS callsign_start,
    STRING(a.callsign_end) AS callsign_end,
    a.match_score2 AS match_score
  FROM (
    SELECT
      *
    FROM (
      SELECT
        *,
        RANK(match_score2) OVER (PARTITION BY row_number ORDER BY match_score2 DESC) AS rank_score
      FROM (
        SELECT
          *,
          CASE WHEN (flag_match = 0
            AND rank_callsign != 0
            AND fishing_msg_ratio > .1) THEN msg_score WHEN (flag_match = 0
            AND rank_name != 0
            AND fishing_msg_ratio > .1) THEN msg_score/3 WHEN (flag_match =1
            AND rank_callsign != 0
            AND fishing_msg_ratio > .1) THEN msg_score*5 WHEN (flag_match = 1
            AND rank_name != 0
            AND fishing_msg_ratio > .1) THEN msg_score ELSE 0 END AS match_score2
        FROM (
          SELECT
            *,
            SUM(callsign_msg_count+name_msg_count/10) AS msg_score
          FROM (
            SELECT
              a.row_number AS row_number,
              a.mmsi AS mmsi,
              a.rank_callsign AS rank_callsign,
              a.rank_name AS rank_name,
              a.callsign_msg_count AS callsign_msg_count,
              a.name_msg_count AS name_msg_count,
              a.callsign_start AS callsign_start,
              a.callsign_end AS callsign_end,
              a.name_start AS name_start,
              a.name_end AS name_end,
              a.MID_code AS MID_code,
              a.Gear_Main_Code AS Gear_Main_Code,
              a.Gear_Sec_Code AS Gear_Sec_Code,
              a.Country_Code AS Country_Code,
              a.MID_flagcode AS MID_flagcode,
              a.flag_match AS flag_match,
              b.fishing_msg_ratio AS fishing_msg_ratio,
            FROM (
              SELECT
                *,
                CASE WHEN Country_Code = MID_flagcode THEN 1 ELSE 0 END AS flag_match
              FROM (
                SELECT
                  a.row_number AS row_number,
                  a.mmsi AS mmsi,
                  a.rank_callsign AS rank_callsign,
                  a.rank_name AS rank_name,
                  a.callsign_msg_count AS callsign_msg_count,
                  a.name_msg_count AS name_msg_count,
                  a.callsign_start AS callsign_start,
                  a.callsign_end AS callsign_end,
                  a.name_start AS name_start,
                  a.name_end AS name_end,
                  a.MID_code AS MID_code,
                  a.Gear_Main_Code AS Gear_Main_Code,
                  a.Gear_Sec_Code AS Gear_Sec_Code,
                  a.Country_Code AS Country_Code,
                  b.Alpha_3 AS MID_flagcode
                FROM (
                  SELECT
                    row_number,
                    mmsi,
                    MAX(rank_callsign) AS rank_callsign,
                    MAX(rank_name) AS rank_name,
                    MAX(callsign_msg_count) AS callsign_msg_count,
                    MAX(name_msg_count) AS name_msg_count,
                    MAX(callsign_start) AS callsign_start,
                    MAX(callsign_end) AS callsign_end,
                    MAX(name_start) AS name_start,
                    MAX(name_end) AS name_end,
                    MID_code,
                    Country_Code,
                    Gear_Main_Code,
                    Gear_Sec_Code
                  FROM (
                    SELECT
                      row_number,
                      mmsi,
                      rank_callsign,
                      rank_name,
                      IFNULL(callsign_msg_count,0) AS callsign_msg_count,
                      IFNULL(name_msg_count,0) AS name_msg_count,
                      callsign_start,
                      callsign_end,
                      name_start,
                      name_end,
                      MID_code,
                      Country_Code,
                      Gear_Main_Code,
                      Gear_Sec_Code
                    FROM (
                      SELECT
                        row_number,
                        mmsi,
                        RANK(msg_count) OVER (PARTITION BY row_number ORDER BY msg_count DESC) AS rank_callsign,
                        msg_count AS callsign_msg_count,
                        first_timestamp AS callsign_start,
                        last_timestamp AS callsign_end,
                        LEFT(STRING(mmsi), 3) AS MID_code,
                        Gear_Main_Code,
                        Gear_Sec_Code,
                        Country_Code
                      FROM (
                        SELECT
                          a.row_number AS row_number,
                          a.callsign,
                          b.callsign,
                          b.first_timestamp AS first_timestamp,
                          b.last_timestamp AS last_timestamp,
                          b.mmsi AS mmsi,
                          b.msg_count AS msg_count,
                          a.Country_Code AS Country_Code,
                          a.Gear_Main_Code AS Gear_Main_Code,
                          a.Gear_Sec_Code AS Gear_Sec_Code
                        FROM (
                          SELECT
                            *
                          FROM
                            [Registry_matching_sources.EU_registry_311215_mod]
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
                              [Registry_matching_sources.EU_registry_311215_mod])
                            AND msg_count > 10) b
                        ON
                          a.callsign = b.callsign)                                //callsign match
                      WHERE
                        mmsi IS NOT NULL ),
                      (
                      SELECT
                        row_number,
                        mmsi,
                        RANK(msg_count) OVER (PARTITION BY row_number ORDER BY msg_count DESC) AS rank_name,
                        msg_count AS name_msg_count,
                        first_timestamp AS name_start,
                        last_timestamp AS name_end,
                        LEFT(STRING(mmsi), 3) AS MID_code,
                        Gear_Main_Code,
                        Gear_Sec_Code,
                        Country_Code
                      FROM (
                        SELECT
                          a.row_number AS row_number,
                          a.calc_normshipname,
                          b.normalized_shipname,
                          b.first_timestamp AS first_timestamp,
                          b.last_timestamp AS last_timestamp,
                          b.mmsi AS mmsi,
                          b.msg_count AS msg_count,
                          a.Country_Code AS Country_Code,
                          a.Gear_Main_Code AS Gear_Main_Code,
                          a.Gear_Sec_Code AS Gear_Sec_Code
                        FROM (
                          SELECT
                            *
                          FROM
                            [Registry_matching_sources.EU_registry_311215_mod]
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
                              [Registry_matching_sources.EU_registry_311215_mod])
                            AND msg_count > 10) b
                        ON
                          a.calc_normshipname = b.normalized_shipname) )                 // Shipname match
                    WHERE
                      mmsi IS NOT NULL )
                  GROUP BY
                    row_number,
                    mmsi,
                    MID_code,
                    Country_Code,
                    Gear_Main_Code,
                    Gear_Sec_Code
                  ORDER BY
                    row_number ASC) a
                LEFT JOIN EACH (
                  SELECT
                    *
                  FROM
                    [scratch_bjorn.MID_code_table]) b
                ON
                  a.MID_code = b.MID ) ) a
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
            row_number,
            mmsi,
            rank_callsign,
            rank_name,
            callsign_msg_count,
            name_msg_count,
            callsign_start,
            callsign_end,
            name_start,
            name_end,
            MID_code,
            MID_flagcode,
            flag_match,
            fishing_msg_ratio,
            Gear_Main_Code,
            Gear_Sec_Code,
            Country_Code )
        WHERE
          flag_match = 1 ) )
    WHERE
      rank_score = 1
      AND match_score2 != 0) a
  LEFT JOIN (
    SELECT
      *
    FROM
      [Registry_matching_sources.EU_registry_311215_mod]) b
  ON
    a.row_number = b.row_number )
WHERE
  callsign_rank != 0
  AND RIGHT(STRING(mmsi), 6) != '000000'

