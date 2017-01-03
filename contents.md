# Treniformis
<a name="contents">
## Contents
</a>
* GFW
    * [ACTIVE_MMSI](link-1)
        - 2012
        - 2013
        - 2014
        - 2015
        - 2016
    * FINE_LABELS
        - 2012
        - 2013
        - 2014
        - 2015
        - 2016
        - ALL_YEARS
    * FISHING_MMSI
        * [KNOWN](link-4)
            - 2014
            - 2015
        * KNOWN_AND_LIKELY
            - 2012
            - 2013
            - 2014
            - 2015
            - 2016
        * [LIKELY](link-6)
            - 2012
            - 2013
            - 2014
            - 2015
            - 2016
    * [SPOOFING_MMSI](link-7)
        - 2012
        - 2013
        - 2014
        - 2015
        - 2016
    * [VESSEL_INFO](link-8)
        - REEFERS

---------
## READMEs

<a name="link-1"></a>
### GFW/ACTIVE_MMSI [[toc]](#contents)

#### Active MMSIs

MMSIs of vessels which are broadcasting during the specified period.  Only
MMSIs with a minimum number of positional reports are included.

--------

<a name="link-4"></a>
### GFW/FISHING_MMSI/KNOWN [[toc]](#contents)

#### Known Fishing Vessels Version 1

List of MMSIs that are known to be fishing vessels based on the presence of the MMSI on one or more 
public registries.

--------

<a name="link-6"></a>
### GFW/FISHING_MMSI/LIKELY [[toc]](#contents)

#### Likely Fishing MMSIs version 2

MMSIs of vessels which declare the vessel type to be 'Fishing' in type 5 or 24 

Based on this query: https://github.com/GlobalFishingWatch/pleuston/issues/28

See the query committed here for the precise definition.  Basically this is
vessels that have > 1000 positional messages in a year and always declare a 
vessel type of 'Fishing'

##### For Reference

###### Some stuff form Bjorn via slack ###

https://globalfishingwatch.slack.com/files/bjorn/F1F3WFX9S/2015_likely_fishing_list_query.sql

https://globalfishingwatch.slack.com/files/bjorn/F1F2U7F2P/2015_known_fishing.sql

https://globalfishingwatch.slack.com/archives/identity-matching/p1465393952000011


###### Other stuff ###

https://github.com/GlobalFishingWatch/pleuston/issues/27

https://github.com/GlobalFishingWatch/vessel-lists/issues/16

https://github.com/SkyTruth/Benthos/issues/390


###### Google Docs ###

https://docs.google.com/document/d/1QnhgyQ3jtGF83a5-4j25hsvPkh6JNT8vGi8ftWx1UUY/edit

https://docs.google.com/spreadsheets/d/12OVeOxg9N1NViKxH4B7nW31-MwAHW_mS3zPBe2kfIuQ/edit#gid=0

--------

<a name="link-7"></a>
### GFW/SPOOFING_MMSI [[toc]](#contents)

#### Spoofing MMSI Version 3

List of MMSIs that experience substantial ID spoofing

By ID spoofing, we mean two or more vessels that are using the same MMSI at the same time. 

All the messages for an MMSI are grouped into sets of tracks that are contiguous spatially and temporally.  
Each continuous track has a unique seg_id field added.  Some tracks contain invalid lan/lon (like 91, 181) and 
are put into a special 'BAD' segment. 

The test for spoofing is fairly naive - we simple compute the extent of each segment in time, add them all up, 
and compare that to the extent of time that the vessel is active.  If the segment time is longer than the 
active time, then we know that some of the segments must overlap, and this is the indication of ID spoofing.

--------

<a name="link-8"></a>
### GFW/VESSEL_INFO [[toc]](#contents)

#### REEFERS.csv

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

--------