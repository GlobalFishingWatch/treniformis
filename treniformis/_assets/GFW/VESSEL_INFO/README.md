
CONSOLIDATED_LISTS.csv
======================

Derived from a combination of various registry lists. Combining
code currently lives in `mussidae`.

Fields:

1. mmsi: MMSI
2. label: type of vessel
3. length: meters
4. engine_power: kilowatts
5: tonnage: gross metric tons
6. split: 'Training' | 'Test' (for CNN classifier)


REEFERS.csv
===========

Fields:

1. mmsi: MMSI
2. imo: IMO (if available)
3. call_sign: vessel callsign
4. width: width of vessel
5. avg_length: average vessel total overall length (LOA) in meters
6. stddev_length: standard deviation of vessel length, meters
7. num_length_sources: number values used to calculate avg and std dev of length
8. avg_gross_tonnage: average vessel gross tonnage
9. stddev_gross_tonnage: standard deviation of gross tonnage (tons)
10. num_gross_tonnage_sources: number of values used to calculate avg and std dev of tonnage
11. dead_weight: vessel deadweight (tons)
12. source: where information from vessel was obtained:

    - CLAV = CLAV registry list (from BQ)
    - ITU = ITU registry list (from BQ)
    - ICCAT = ICCAT registry (Dahlhousie students)
    - WCPFC = Western and Central Pacific Tuna Commision registry
    - FFA = FFA registry (from BQ)
    - CCSBT = CCSBT registries (Dahlhousie students)
    - encounters = vessels identified from encounters, information from MarineTraffic
            
13. flag_state: flag state of vessel (from MID codes)