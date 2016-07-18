"""MVP API

The `build_combined_fishign_list()` function seeks to replace the description
below, which was copied from the likely fishing dataset's readme.

    Likely Fishing
    ==============

    Needs a description.


    Migration
    ---------

    Files that were deleted during the migration from `vessel-lists`, but whose
    content needs to be preserved.


    ### make-published.py ###

    ```python
    # Combine multiple mmsi lists to produce the final known-likely fishing vessel lists
    # that are used to determine which vessels are treated as fishing vessels
    known_likely_lists = [
        {'output': 'known-likely-fishing-mmsis-2012.txt',
         'include': [
            '../known-fishing/known-fishing-v1/known-fishing-2014-v1.txt',
            '../exported/likely-fishing/likely-fishing-v2/likely-fishing-2012-v2.txt'
         ],
         'filter': '../exported/active-mmsis/active-mmsis-v1/active-mmsis-2012-v1.txt'
         },

        {'output': 'known-likely-fishing-mmsis-2013.txt',
         'include': [
            '../known-fishing/known-fishing-v1/known-fishing-2014-v1.txt',
            '../exported/likely-fishing/likely-fishing-v2/likely-fishing-2013-v2.txt'
         ],
         'filter': '../exported/active-mmsis/active-mmsis-v1/active-mmsis-2013-v1.txt'
         },

        {'output': 'known-likely-fishing-mmsis-2014.txt',
         'include': [
            '../known-fishing/known-fishing-v1/known-fishing-2014-v1.txt',
            '../exported/likely-fishing/likely-fishing-v2/likely-fishing-2014-v2.txt'
         ],
         'filter': '../exported/active-mmsis/active-mmsis-v1/active-mmsis-2014-v1.txt'
         },

        {'output': 'known-likely-fishing-mmsis-2015.txt',
         'include': [
            '../known-fishing/known-fishing-v1/known-fishing-2015-v1.txt',
            '../exported/likely-fishing/likely-fishing-v2/likely-fishing-2015-v2.txt'
         ],
         'filter': '../exported/active-mmsis/active-mmsis-v1/active-mmsis-2015-v1.txt'
         },

        {'output': 'known-likely-fishing-mmsis-2016.txt',
         'include': [
            '../known-fishing/known-fishing-v1/known-fishing-2015-v1.txt',
            '../exported/likely-fishing/likely-fishing-v2/likely-fishing-2016-v2.txt'
         ],
         'filter': '../exported/active-mmsis/active-mmsis-v1/active-mmsis-2016-v1.txt'
         },
    ]


    for item in known_likely_lists:
        mmsis = set()

        for source in item['include']:
            with open(source, 'r') as f:
                mmsis |= {mmsi for mmsi in f}

        with open(item['filter']) as f:
            mmsis &= {mmsi for mmsi in f}

        mmsis = sorted(list(mmsis))

        with open(item['output'], 'w') as outfile:
            for mmsi in mmsis:
                outfile.write(mmsi)
    ```
"""


import os

import six

from treniformis import errors


def get_annual_list_path(asset_id):
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

    asset_path = os.path.join(*asset_id.rstrip('/').split('/'))
    path = os.path.join(
        os.path.dirname(__file__), '_assets', '{}.txt'.format(asset_path))

    if not os.path.exists(path) or not os.path.isfile(path):
        raise errors.TreniformisIOError(
            "Invalid asset ID: {}".format(asset_id))

    return path


def build_combined_fishing_list(year):
    """Build the GFW combined fishing list.

    Parameters
    ----------
    year : int
        Process data for this year.

    Returns
    -------
    set
        MMSIs.
    """

    if year < 2014:
        known_year = 2014
    else:
        known_year = year

    known_fishing_id = 'GFW/FISHING_MMSI/KNOWN/{}'.format(known_year)
    likely_fishing_id = 'GFW/FISHING_MMSI/LIKELY/{}'.format(year)
    active_mmsis_id = 'GFW/ACTIVE_MMSI/{}'.format(year)

    known_path = get_annual_list_path(known_fishing_id)
    likely_path = get_annual_list_path(likely_fishing_id)
    active_path = get_annual_list_path(active_mmsis_id)

    mmsis = set()
    for p in known_path, likely_path:
        with open(p) as f:
            stripped = six.moves.map(lambda x: x.strip(), f)
            mmsis |= set(stripped)

    with open(active_path) as f:
        stripped = six.moves.map(lambda x: x.strip(), f)
        mmsis &= set(stripped)

    return mmsis
