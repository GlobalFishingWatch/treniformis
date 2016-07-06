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
    [('GFW/ACTIVE_MMSIS/{}'.format(y), pjoin(BASEDIR, 'GFW', 'ACTIVE_MMSIS', '{}.txt'.format(y))) for y in YEARS] +
    [('GFW/FISHING/LIKELY/{}'.format(y), pjoin(BASEDIR, 'GFW', 'FISHING', 'LIKELY', '{}.txt'.format(y))) for y in YEARS] +
    [('GFW/SPOOFING/{}'.format(y), pjoin(BASEDIR, 'GFW', 'SPOOFING', '{}.txt'.format(y))) for y in YEARS] +
    [('GFW/WKV/FISHING/KNOWN/{}'.format(y), pjoin(BASEDIR, 'GFW', 'WKV', 'FISHING', 'KNOWN', '{}.txt'.format(y))) for y in (2014, 2015)] +
    [('GFW/WKV/FISHING/LIKELY/{}'.format(y), pjoin(BASEDIR, 'GFW', 'WKV', 'FISHING', 'LIKELY', '{}.txt'.format(y))) for y in (2014, 2015)]
)
def test_list_exists(asset_id, expected):
    actual = treniformis.get_annual_list_path(asset_id)
    assert expected == actual
    assert os.path.exists(actual)
    assert os.path.exists(expected)


def test_get_annual_list_path_exception():
    with pytest.raises(errors.TreniformisIOError):
        treniformis.get_annual_list_path('INVALID_ID')
