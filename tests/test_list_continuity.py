"""This project requires distributing files that will change over time, so to
keep the git diffs small and efficient we run some tests on the lists to ensure
they remain sorted and unique.
"""


import os
import csv

import pytest

import treniformis


def _get_mmsi_lists():
    """Yields paths to files containing lists of MMSIs."""
    base = os.path.join(os.path.dirname(treniformis.__file__), '_assets')
    for root, dirs, files in os.walk(base):
        for name in files:
            if os.path.splitext(name)[1].lower() == '.txt':
                yield os.path.join(root, name)


# Files that should not be included in _get_csv_lists
CSV_BLACKLIST = set()

def _get_csv_lists():
    "Yields paths to files containing CSVs with a column named `mmsi`"
    base = os.path.join(os.path.dirname(treniformis.__file__), '_assets')
    for root, dirs, files in os.walk(base):
        for name in files:
            if name not in CSV_BLACKLIST and os.path.splitext(name)[1].lower() == '.csv':
                yield os.path.join(root, name)


def is_sorted(iterable):
    iterable = iter(iterable)
    prev = next(iterable)
    for item in iterable:
        if prev > item:
            return False
        else:
            prev = item
    return True


def test_is_sorted():
    assert is_sorted(range(5))
    assert not is_sorted(reversed(range(5)))
    assert is_sorted(['0', '1', '10', '2'])
    assert not is_sorted(['10', '0', '1', '2'])


@pytest.mark.parametrize("path", _get_mmsi_lists())
def test_mmsi_list_sorted(path):
    """MMSI lists should remain sorted."""
    with open(path) as f:
        assert is_sorted(f)


@pytest.mark.parametrize("path", _get_mmsi_lists())
def test_mmsi_list_unique(path):
    """MMSI lists should not contain duplicates."""
    with open(path) as f:
        stripped = [l.strip() for l in f]
        assert len(stripped) == len(set(stripped))

def _mmsi_reader(f):
    reader = csv.DictReader(f)
    for x in reader:
        yield x['mmsi'].strip()

@pytest.mark.parametrize("path", _get_csv_lists())
def test_csv_list_sorted(path):
    """CSV lists should remain sorted by MMSI."""
    with open(path) as f:
        assert is_sorted(_mmsi_reader(f))


@pytest.mark.parametrize("path", _get_mmsi_lists())
def test_mmsi_list_unique(path):
    """MMSI lists should not contain duplicates."""
    with open(path) as f:
        stripped = [l.strip() for l in f]
        assert len(stripped) == len(set(stripped))


@pytest.mark.parametrize("path", _get_csv_lists())
def test_csv_list_unique(path):
    """CSV lists should not contain duplicate MMSI."""
    with open(path) as f:
        mmsi = list(_mmsi_reader(f))
        assert len(mmsi) == len(set(mmsi))
