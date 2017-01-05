"""Unittests for the MVP API"""


import os.path
from os.path import join as pjoin

import pytest

import treniformis
from treniformis import errors


BASEDIR = os.path.dirname(treniformis.__file__)
BASEDIR = pjoin(BASEDIR, '_assets')
YEARS = (2012, 2013, 2014, 2015, 2016)


@pytest.mark.parametrize("asset_id",
    ['GFW/ACTIVE_MMSI/{}'.format(y) for y in YEARS] +
    ['GFW/FISHING_MMSI/KNOWN/{}'.format(y) for y in (2014, 2015)] +
    ['GFW/FISHING_MMSI/LIKELY/{}'.format(y) for y in YEARS] +
    ['GFW/SPOOFING_MMSI/{}'.format(y) for y in YEARS]
)
def test_list_exists(asset_id):
    for row in treniformis.get_annual_list(asset_id):
        return
    assert False

def test_get_annual_list_exception():
    with pytest.raises(errors.TreniformisIOError):
        treniformis.get_annual_list('INVALID_ID')


@pytest.mark.parametrize("year", range(2012, 2016))
def test_build_combined_fishing_list_clean(year):
    """Combined fishing lists for >= 2014 are easy to test.

    Lists < 2014 are complicated because we don't have known fishing lists.
    Instead we always use the 2014 known list and merge with the actual years
    for everything else."""

    if year < 2014:
        known_year = 2014
    else:
        known_year = year

    with treniformis.get_annual_list(
        'GFW/FISHING_MMSI/KNOWN/{}'.format(known_year)) as f:
        known_mmsis = set((l.strip() for l in f))
    with treniformis.get_annual_list(
        'GFW/FISHING_MMSI/LIKELY/{}'.format(year)) as f:
        likely_mmsis = set((l.strip() for l in f))
    with treniformis.get_annual_list(
        'GFW/ACTIVE_MMSI/{}'.format(year)) as f:
        active_mmsis = set((l.strip() for l in f))

    expected = (known_mmsis | likely_mmsis) & active_mmsis
    actual = treniformis.build_combined_fishing_list(year)
    assert actual == expected


def test_build_combined_fishing_list_string():
    # just make sure we get a non-empty result with a string param
    assert treniformis.build_combined_fishing_list('2013')

