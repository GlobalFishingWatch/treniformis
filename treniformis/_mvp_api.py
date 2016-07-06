"""MVP API"""


import os

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

    path = os.path.join(
        os.path.dirname(__file__), '_assets', '{}.txt'.format(asset_id))
    if not os.path.exists(path) or not os.path.isfile(path):
        raise errors.TreniformisIOError(
            "Invalid asset ID: {}".format(asset_id))

    return path
