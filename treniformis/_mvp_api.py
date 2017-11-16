"""MVP API
Generates lists of MMSIs based on the files in _assets

Example usage:

    import treniformis
    with treniformis.get_annual_list('GFW/FISHING_MMSI/KNOWN_AND_LIKELY/2016') as f:
      for mmsi in f:
        print mmsi

"""


import os

import six

from treniformis import errors
from pkg_resources import resource_stream

def open(p):
    try:
        return resource_stream("treniformis", '_assets/' + p)
    except IOError:
        raise errors.TreniformisIOError(p)

def get_annual_list(p):
    try:
        return resource_stream("treniformis", '_assets/' + p + '.txt')
    except IOError:
        raise errors.TreniformisIOError(p)

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

    year = int(year)
    known_year = "ALL_YEARS"

    known_fishing_id = 'GFW/FISHING_MMSI/KNOWN/{}'.format(known_year)
    likely_fishing_id = 'GFW/FISHING_MMSI/LIKELY/{}'.format(year)
    active_mmsis_id = 'GFW/ACTIVE_MMSI/{}'.format(year)

    mmsis = set()
    for p in known_fishing_id, likely_fishing_id:
        with get_annual_list(p) as f:
            stripped = six.moves.map(lambda x: x.strip(), f)
            mmsis |= set(stripped)

    with get_annual_list(active_mmsis_id) as f:
        stripped = six.moves.map(lambda x: x.strip(), f)
        mmsis &= set(stripped)

    return mmsis
