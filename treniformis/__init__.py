"""

MMSI Lists
----------

The following attributes are dict-like objects that contain lists
of MMSI, typically indexed by year. Documentation 
is available for them using `help(obj)` or `print(obj.__doc__)`:

* active_mmsis: MMSI asociated with a significant number of AIS 
  messages


* known_fishing: vessels known to be fishing based on lists or manual 
  classification


* likely_fishing: vessels likely fishing based on AIS messages


* known_likely_fishing: combination of known and likely MMSI lists

    
* spoofing: MMSI that appear to be associated with spoofing.


Additional Items
----------------

vessel_classes: list of classes used in manual and NNet classification

clasification_lists_path: path to directory of miscelaneous classification lists


In addition to the stuff documented above there are many items
installed in `internal` that are primarily used as the sources
for the publised lists. Or are old and are kept around for reference
"""


from treniformis._mvp_api import get_annual_list


__version__ = '0.0.1'
__author__ = 'Global Fishing Watch'
__email__ = 'info@globalfishingwatch.org'
__source__ = 'https://github.com/GlobalFishingWatch/treniformis'
__license__ = """
Copyright 2016 SkyTruth
Authors: Global Fishing Watch

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
