from __future__ import print_function

vl_base = "../vessel-lists/"
t_base = "treniformis/_assets/"

all_years = [2012, 2013, 2014, 2015, 2016]

tests = [
    ("exported/active-mmsis/active-mmsis-v1/active-mmsis-{}-v1.txt",
     "GFW/ACTIVE_MMSI/{}.txt", all_years),
    ("exported/likely-fishing/likely-fishing-v2/likely-fishing-{}-v2.txt",
     "GFW/FISHING_MMSI/LIKELY/{}.txt", all_years),
     # There isn't an existing script to test against
#     ("exported/spoofing/spoofing-mmsis-v3/spoofing-mmsi-{}-v3.txt",
#      "GFW/SPOOFING_MMSI/{}.txt", all_years),
    ("known-fishing/known-fishing-v1/known-fishing-{}-v1.txt",
     "GFW/FISHING_MMSI/KNOWN/{}.txt", [2014, 2015]),
    ('published/known-likely-fishing-mmsis-{}.txt',
     'GFW/FISHING_MMSI/KNOWN_AND_LIKELY/{}.txt', all_years)
]


for vl_path, t_path, years in tests:
    for y in years:
        vl_mmsi = set(open(vl_base + vl_path.format(y)).read().strip().split())
        t_mmsi = set(open(t_base + t_path.format(y)).read().strip().split())
        difference = sorted(vl_mmsi.symmetric_difference(t_mmsi))
        if difference:
            print(t_path.format(y), "differs at:")
            if len(difference) < 8:
                print("    ", difference)
            else:
                print("    ", difference[:8], "+", len(difference) - 8, "others")
