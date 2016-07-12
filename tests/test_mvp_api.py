"""Unittests for the MVP API"""


import os.path
from os.path import join as pjoin

import pytest

import treniformis
from treniformis import errors


BASEDIR = os.path.dirname(treniformis.__file__)
BASEDIR = pjoin(BASEDIR, '_assets')
YEARS = (2012, 2013, 2014, 2015, 2016)


@pytest.mark.parametrize("asset_id,expected",
    [('GFW/ACTIVE_MMSI/{}'.format(y), pjoin(BASEDIR, 'GFW', 'ACTIVE_MMSI', '{}.txt'.format(y))) for y in YEARS] +
    [('GFW/FISHING_MMSI/KNOWN/{}'.format(y), pjoin(BASEDIR, 'GFW', 'FISHING_MMSI', 'KNOWN', '{}.txt'.format(y))) for y in (2014, 2015)] +
    [('GFW/FISHING_MMSI/LIKELY/{}'.format(y), pjoin(BASEDIR, 'GFW', 'FISHING_MMSI', 'LIKELY', '{}.txt'.format(y))) for y in YEARS] +
    [('GFW/SPOOFING_MMSI/{}'.format(y), pjoin(BASEDIR, 'GFW', 'SPOOFING_MMSI', '{}.txt'.format(y))) for y in YEARS]
)
def test_list_exists(asset_id, expected):
    actual = treniformis.get_annual_list_path(asset_id)
    assert expected == actual
    assert os.path.exists(actual)
    assert os.path.exists(expected)


def test_get_annual_list_path_exception():
    with pytest.raises(errors.TreniformisIOError):
        treniformis.get_annual_list_path('INVALID_ID')


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

    known_path = treniformis.get_annual_list_path(
        'GFW/FISHING_MMSI/KNOWN/{}'.format(known_year))
    likely_path = treniformis.get_annual_list_path(
        'GFW/FISHING_MMSI/LIKELY/{}'.format(year))
    active_path = treniformis.get_annual_list_path(
        'GFW/ACTIVE_MMSI/{}'.format(year))

    with open(known_path) as f:
        known_mmsis = set((l.strip() for l in f))
    with open(likely_path) as f:
        likely_mmsis = set((l.strip() for l in f))
    with open(active_path) as f:
        active_mmsis = set((l.strip() for l in f))

    expected = (known_mmsis | likely_mmsis) & active_mmsis
    actual = treniformis.build_combined_fishing_list(year)
    assert actual == expected
