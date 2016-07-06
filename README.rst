treniformis
===========

Repository of lists of vessels by type as compiled by
Global-Fishing-Watch

...

- Installation, etc

- Point to readme in Repo


This repository will contain three categories of lists.

1. **Likely fishing lists** - lists generated from a query of vessels identifying themselves as fishing in the shiptype_text field in the vessel identity messages in the type 5 and type 24 AIS messages. Details of the query can be found in Benthos #397. In the next round we will filter out some additional "unknown" vessel types and probably drop the threshold to include some vessels that almost always identify themselves as fishing.
  - *Likelyfishing_2014.csv* - Vessels which always identified themselves as fishing throughout 2014
2. **Known fishing lists** - list based on public fishing registry records. A list of registries can be found [here](https://docs.google.com/spreadsheets/d/15ICZzrkiaPPWV7sp0uytNnwXGRM8jTh6KjJ4026lDGU/edit?usp=sharing).
3. **Combined fishing lists** - Lists produced by combining likely and known fishing lists and then removing sets of known non-fishing vessels (fish carriers, fishspotting helicopters, research vessels) along with short mmsi's (less than 5 digits)  and mmsi's that will likely have a large number of spoofing vessels (111111111). See Benthos #397.
  - *Combinedfishing_2014.csv* - from Likelyfishing_2014 and the FFA, CLAV, and CCAMLR registries as described in Benthos #397.
  - *Combinedfishing_2013.csv* - from a an identical query to that used for the Likelyfishing_2014 list but using a 2013 date range. The same registry sources were added in, see Benthos #370. It is difficult to get registry data from previous years, 2014 records were added to this list.


Vessel Classes
--------------

Longliner
Pots and traps
Purse seiner
Squid vessel
Trawler
Cargo/Tanker
Motorized Yacht/Pleasure Craft
Research/Survey
Seismic vessel
Passenger vessel: ferries
Sail boat
Work vessel: tug, pilot, supply, dredgers, military, patrol
