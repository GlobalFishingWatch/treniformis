import os
import yaml
from collections import namedtuple


this_dir = os.path.dirname(os.path.abspath(__file__))
top_dir = os.path.abspath(os.path.join(this_dir, ".."))
asset_dir = os.path.join(top_dir, "treniformis/_assets")

config_path = os.path.join(this_dir, "update_filter_lists_config.yml")
with open(config_path) as f:
    config = yaml.load(f)

default_date_ranges = config['default_date_ranges']

FilterList = namedtuple("FilterList",  ["path", "sql", "date_ranges"])

filter_lists = [
    FilterList("GFW/ACTIVE_MMSI", "active-mmsis", default_date_ranges),
    FilterList("GFW/SPOOFING_MMSI", "spoofing-mmsis", default_date_ranges),
    FilterList("GFW/FISHING_MMSI/LIKELY", "likely-fishing", default_date_ranges),
]

filter_lists_2 = [
    FilterList("GFW/ID_MAPS/mmsi-to-vessel-id.csv", "mmsi-to-vessel-id", None),
]
