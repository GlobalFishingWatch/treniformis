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


import os


def get_annual_list(asset_id):
    """Get a path to an MMSI list, which is probably a text file with a single
    MMSI per line.

    This is an MVP API that will almost certainly be deprecated at some point.
    Do not construct file paths directly.

    Parameters
    ----------
    asset_id : str
        Like ``GFW/WKV/KNOWN_FISHING/2014``.

    Returns
    -------
    str
        File path.
    """
    return os.path.join(os.path.dirname(__file__), '{}.txt'.format(asset_id))
