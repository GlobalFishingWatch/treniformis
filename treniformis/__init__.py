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


import glob
import os


def _path(*subpaths):
    here = os.path.dirname(__file__)
    return os.path.join(here, *subpaths)


def _load_mmsis_by_year(
        name, path, year_index, pattern="*.txt", readme="README.md"):

    if readme:
        with open(_path(path, readme)) as f:
            doc = f.read()
    else:
        doc = None
    mmsi_map = type(name, (dict,), {"__doc__": doc})
    paths = glob.glob(_path(path, pattern))
    mmsi_map = mmsi_map()
    for p in paths:
        name, _ = os.path.splitext(os.path.basename(p))
        year = int(name.split('-')[year_index])
        mmsi = [x.strip() for x in open(p).read().strip().split('\n')]
        mmsi_map[year] = mmsi
    return mmsi_map


def _load_list(name, path, readme=None):
    if readme:
        with open(_path(path, readme)) as f:
            doc = f.read()
    else:
        doc = None
    list_like = type(name, (list,), {"__doc__": doc})
    full_path = _path(path, name)
    with open(full_path).read() as f:
        lines = f.splitlines()
    return list_like([x.strip() for x in lines])


active_mmsis = _load_mmsis_by_year(
    name="active_mmsis",
    path="exported/active-mmsis/active-mmsis-v1",
    year_index=2)

known_fishing = _load_mmsis_by_year(
    name="known_fishing",
    path="known-fishing/known-fishing-v1",
    year_index=2)

likely_fishing = _load_mmsis_by_year(
    name="likely_fishing",
    path="exported/likely-fishing/likely-fishing-v2",
    year_index=2)

spoofing = _load_mmsis_by_year(
    name="spoofing",
    path="exported/spoofing/spoofing-mmsis-v3",
    year_index=2)

known_likely_fishing = _load_mmsis_by_year(
    name="known_likely_fishing",
    path="published",
    year_index=4,
    pattern="known-likely-fishing-mmsis-*.txt",
    readme=None)


vessel_classes = _load_list(
    name="vessel_classes.md",
    path="",
    readme=None)

classification_lists_path = _path("internal/classification_lists")
