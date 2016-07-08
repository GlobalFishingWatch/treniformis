Likely Fishing
==============

Needs a description.


Migration
---------

Files that were deleted during the migration from `vessel-lists`, but whose
content needs to be preserved.


### make-published.py ###

```python
"""
Combine multiple mmsi lists to produce the final known-likely fishing vessel lists
that are used to determine which vessels are treated as fishing vessels
"""

known_likely_lists = [
    {'output': 'known-likely-fishing-mmsis-2012.txt',
     'include': [
        '../known-fishing/known-fishing-v1/known-fishing-2014-v1.txt',
        '../exported/likely-fishing/likely-fishing-v2/likely-fishing-2012-v2.txt'
     ],
     'filter': '../exported/active-mmsis/active-mmsis-v1/active-mmsis-2012-v1.txt'
     },

    {'output': 'known-likely-fishing-mmsis-2013.txt',
     'include': [
        '../known-fishing/known-fishing-v1/known-fishing-2014-v1.txt',
        '../exported/likely-fishing/likely-fishing-v2/likely-fishing-2013-v2.txt'
     ],
     'filter': '../exported/active-mmsis/active-mmsis-v1/active-mmsis-2013-v1.txt'
     },

    {'output': 'known-likely-fishing-mmsis-2014.txt',
     'include': [
        '../known-fishing/known-fishing-v1/known-fishing-2014-v1.txt',
        '../exported/likely-fishing/likely-fishing-v2/likely-fishing-2014-v2.txt'
     ],
     'filter': '../exported/active-mmsis/active-mmsis-v1/active-mmsis-2014-v1.txt'
     },

    {'output': 'known-likely-fishing-mmsis-2015.txt',
     'include': [
        '../known-fishing/known-fishing-v1/known-fishing-2015-v1.txt',
        '../exported/likely-fishing/likely-fishing-v2/likely-fishing-2015-v2.txt'
     ],
     'filter': '../exported/active-mmsis/active-mmsis-v1/active-mmsis-2015-v1.txt'
     },
    
    {'output': 'known-likely-fishing-mmsis-2016.txt',
     'include': [
        '../known-fishing/known-fishing-v1/known-fishing-2015-v1.txt',
        '../exported/likely-fishing/likely-fishing-v2/likely-fishing-2016-v2.txt'
     ],
     'filter': '../exported/active-mmsis/active-mmsis-v1/active-mmsis-2016-v1.txt'
     },
]


for item in known_likely_lists:
    mmsis = set()

    for source in item['include']:
        with open(source, 'r') as f:
            mmsis |= {mmsi for mmsi in f}

    with open(item['filter']) as f:
        mmsis &= {mmsi for mmsi in f}

    mmsis = sorted(list(mmsis))

    with open(item['output'], 'w') as outfile:
        for mmsi in mmsis:
            outfile.write(mmsi)
```
