treniformis
===========

Global Fishing Watch vessel lists.  Very alpha.

.. image:: https://travis-ci.com/GlobalFishingWatch/treniformis.svg?token=tu7qmzYG3ruJYdnto4aT&branch=master
    :target: https://travis-ci.com/GlobalFishingWatch/treniformis


Example
-------

.. code-block:: python

    import treniformis
    with treniformis.get_annual_list('GFW/FISHING_MMSI/KNOWN_AND_LIKELY/2016') as f:
      for mmsi in f:
        print mmsi

Developing
----------

.. code-block:: console

    $ git clone https://github.com/GlobalFishingWatch/treniformis
    $ cd treniformis
    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install -e .\[all\]
    $ py.test --cov treniformis --cov-report term-missing


Lists
-----

Likely Fishing
~~~~~~~~~~~~~~

Generated from a query of vessels identifying themselves as fishing in the
``shiptype_text`` field in the vessel identity messages in the type 5 and type
24 AIS messages. Details of the query can be found in Benthos #397. In the next
round we will filter out some additional "unknown" vessel types and probably
drop the threshold to include some vessels that almost always identify
themselves as fishing.

Known Fishing
~~~~~~~~~~~~~
Based on `public fishing registry records <https://docs.google.com/spreadsheets/d/15ICZzrkiaPPWV7sp0uytNnwXGRM8jTh6KjJ4026lDGU/edit?pref=2&pli=1#gid=1259036802>`_.

Combined Fishing
~~~~~~~~~~~~~~~~

Produced by combining likely and known fishing lists and then removing sets of
known non-fishing vessels (fish carriers, fishspotting helicopters, research
vessels) along with short mmsi's (less than 5 digits)  and mmsi's that will
likely have a large number of spoofing vessels (111111111). See Benthos #397.


Vessel Classes
--------------

* Longliner
* Pots and traps
* Purse seiner
* Squid vessel
* Trawler
* Cargo/Tanker
* Motorized Yacht/Pleasure Craft
* Research/Survey
* Seismic vessel
* Passenger vessel: ferries
* Sail boat
* Work vessel: tug, pilot, supply, dredgers, military, patrol


License
-------

See `LICENSE.txt <LICENSE.txt>`_