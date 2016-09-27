"""Treniformis: Global Fishing Watch vessel lists

Currently the API only produces paths to files, which should only be constructed
like:

    >>> import treniformis
    >>> treniformis.get_annual_list('GFW/FISHING_MMSI/LIKELY/2013')
    '.../_assets/GFW/FISHING_MMSI/LIKELY/2013.txt'

and never directly constructed.  See the README for more information.

In addition the dictionary `available_assets` contains descriptions of
the available assets.  Printing `available_assets` will shows a
summary of available assets, while printing the individual entries
will show more detailed descriptions:

    >>> treniformis.available_assets
    {'GFW/ACTIVE_MMSI': GFW/ACTIVE_MMSI/[2012|2013|2014|2015|2016],
     'GFW/FISHING_MMSI/KNOWN': GFW/FISHING_MMSI/KNOWN/[2014|2015],
     'GFW/FISHING_MMSI/KNOWN_AND_LIKELY': GFW/FISHING_MMSI/KNOWN_AND_LIKELY/[2012|2013|2014|2015|2016],
     'GFW/FISHING_MMSI/LIKELY': GFW/FISHING_MMSI/LIKELY/[2012|2013|2014|2015|2016],
     'GFW/SPOOFING_MMSI': GFW/SPOOFING_MMSI/[2012|2013|2014|2015|2016]}
     
    >>> print(treniformis.availabl_assets['GFW/ACTIVE_MMSI'])
    **GFW/ACTIVE_MMSI**
        
    Available
    ---------
    GFW/ACTIVE_MMSI/2012
    GFW/ACTIVE_MMSI/2013
    GFW/ACTIVE_MMSI/2014
    GFW/ACTIVE_MMSI/2015
    GFW/ACTIVE_MMSI/2016

    Description
    -----------
    MMSIs of vessels which are broadcasting during the specified period.  Only
    MMSIs with a minimum number of positional reports are included.


https://github.com/GlobalFishingWatch/treniformis
"""


from treniformis._mvp_api import get_annual_list_path
from treniformis._mvp_api import create_asset_descriptions as _createdesc

available_assets = _createdesc()



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
