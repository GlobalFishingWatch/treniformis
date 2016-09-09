"""Treniformis: Global Fishing Watch vessel lists

Currently the API only produces paths to files, which should only be constructed
like:

    import treniformis
    treniformis.get_annual_list('GFW/WKV/FISHING/LIKELY')

and never directly constructed.  See the readme for more information.

https://github.com/GlobalFishingWatch/treniformis
"""


from treniformis._mvp_api import build_combined_fishing_list
from treniformis._mvp_api import get_annual_list_path


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
