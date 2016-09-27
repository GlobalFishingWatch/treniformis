"""MVP API


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


class AssetClass:

    def __init__(self, path, description, item_names):
        self.description = description
        self.path = path
        self.item_names = item_names
        
    def __str__(self):
        paths = ["{0}/{1}".format(self.path, x) for x in self.item_names]
        available = '\n'.join(paths)
        return """**{path}**
        
Available
---------
{available}

Description
-----------
{description}""".format(path=self.path, 
                                available=available, 
                                description=self.description)
                                
    def __repr__(self):
        names = "|".join([x.rsplit(".", 1)[0] for x in self.item_names])
        return "{path}/[{names}]".format(path=self.path, names=names)

        
    
def create_asset_descriptions():
    base = os.path.join(os.path.dirname(__file__), '_assets')
    assets = {}
    for root, dirs, files in os.walk(base):
        if "README.md" in files:
            with open(os.path.join(root, "README.md")) as f:
                descr = f.read().strip()
            names = [x.lstrip(os.sep).rsplit(".", 1)[0] for x in files if x != "README.md"]
            path = root.rsplit("_assets", 1)[-1].replace(os.sep, "/").lstrip("/")
            assets[path] = AssetClass(path, descr, names)
    return assets



