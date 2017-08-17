Changes
=======

Higher level changes affecting the API or data.

0.6
---

# [`#67`](https://github.com/GlobalFishingWatch/treniformis/pull/67)
  Update pipeline file we are using and switch to using classify for
  all queries.


0.5
---

# [`#62`](https://github.com/GlobalFishingWatch/treniformis/pull/62/files)
  Automate updating of sub-versions (only dates change)

# [`#61`](https://github.com/GlobalFishingWatch/treniformis/pull/61)
  
   * Add CONSOLIDATED_LISTS from (same as nnet training lists)

   * Use consolidated lists to derive KNOWN_FISHING and KNOWN_NONFISHING

   * Remove KNOWN_NONFISHING from KNOWN_AND_LIKELY fishing

0.4
---

* [`#49`](https://github.com/GlobalFishingWatch/treniformis/pull/49)
  Allow `treniformis` to be installed as an egg.


0.3 - 2017-01-04
----------------

* [`#47`](https://github.com/GlobalFishingWatch/treniformis/pull/47)
  Move SQL version numbers into the SQL files as comments

* [`#48`](https://github.com/GlobalFishingWatch/treniformis/pull/48)
  Add vessels with more than 500 points per year.

* [`#53`](https://github.com/GlobalFishingWatch/treniformis/pull/53)
  Add type 19 messages to active vessels query; update dates and include 2017
  as a 12 month window.


0.2 - 2016-10-14
----------------

* [`#31`](https://github.com/GlobalFishingWatch/treniformis/pull/31)
  Parameterize table names.

* [`#33`](https://github.com/GlobalFishingWatch/treniformis/pull/33)
  Change tables referenced to `pipeline_740` and update lists.

* [`#39`](https://github.com/GlobalFishingWatch/treniformis/pull/39)
  Add reefers list

* [`#40`](https://github.com/GlobalFishingWatch/treniformis/pull/40)
  Parameterize dates

* [`#41`](https://github.com/GlobalFishingWatch/treniformis/pull/41)
  Update date ranges to include dates through October 2016

* [`#43`](https://github.com/GlobalFishingWatch/treniformis/pull/43)
  Add version info to init
  

0.1 - 2016-09-09
----------------

* [`#17`](https://github.com/GlobalFishingWatch/treniformis/pull/17)
  [`#19`](https://github.com/GlobalFishingWatch/treniformis/pull/19)
  Add scripts to automatically refresh lists from BigQuery.
  
* [`#19`](https://github.com/GlobalFishingWatch/treniformis/pull/19)
  Exclude Helicopters and fix dates

* [`#20`](https://github.com/GlobalFishingWatch/treniformis/pull/22)
  Uniquiefy lists
  
* [`#24`](https://github.com/GlobalFishingWatch/treniformis/pull/24)
  Add machinery for creating versioned releases.


0.0.1 - 2016-07-18
----------------

* [`#13`](https://github.com/GlobalFishingWatch/treniformis/pull/13)
  Migration from `vessel-lists` repo.
