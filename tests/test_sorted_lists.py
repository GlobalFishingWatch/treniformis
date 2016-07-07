"""This project requires distributing files that will change over time, so to
keep the git diffs small and efficient we ensure the files remain sorted.
"""


import os

import pytest

import treniformis


def _get_mmsi_lists():
    """Yields paths to files containing lists of MMSIs."""
    base = os.path.join(os.path.dirname(treniformis.__file__), '_assets')
    for root, dirs, files in os.walk(base):
        for name in files:
            if os.path.splitext(name)[1].lower() == '.txt':
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
    with open(path) as f:
        assert is_sorted(f)
