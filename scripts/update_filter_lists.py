from __future__ import print_function
import bqtools
import treniformis
import os
import six
import csv
from utility import this_dir
from utility import top_dir
from utility import asset_dir
from utility import default_date_ranges
from utility import filter_lists
from utility import config

def copy_to_sorted_mmsi(source_path, dest_path):
    """
    Drop header (1st row) and sort then dump to dest_path
    """
    lines = []
    with open(source_path) as source:
        for i, l in enumerate(source.readlines()):
            l = l.strip()
            if i < 1 or not l:
                continue
            lines.append(l)     
    lines = sorted(set(lines)) 
    lines.sort()  
    with open(dest_path, "w") as dest:
        dest.write('\n'.join(lines))


def build_combined_fishing_list(base_path, year):
    """Build the GFW combined fishing list.

    Parameters
    ----------
    year : int
        Process data for this year.

    Returns
    -------
    list
        sorted MMSIs.
    """

        
    known_fishing_path = 'GFW/FISHING_MMSI/KNOWN/ALL_YEARS.txt'
    known_nonfishing_path = 'GFW/FISHING_MMSI/KNOWN/ALL_YEARS.txt'
    likely_path = 'GFW/FISHING_MMSI/LIKELY/{}.txt'.format(year)
    active_path = 'GFW/ACTIVE_MMSI/{}.txt'.format(year)

    mmsis = set()
    for p in known_fishing_path, likely_path:
        with open(os.path.join(base_path, p)) as f:
            stripped = six.moves.map(lambda x: x.strip(), f)
            mmsis |= set(stripped)

    with open(os.path.join(base_path, known_nonfishing_path)) as f:
        stripped = six.moves.map(lambda x: x.strip(), f)
        mmsis -= set(stripped)      

    with open(os.path.join(base_path, active_path)) as f:
        stripped = six.moves.map(lambda x: x.strip(), f)
        mmsis &= set(stripped)

    return sorted(mmsis)


proj_id = "world-fishing-827"
gcs_path_template = 'gs://world-fishing-827/scratch/treniformis/temp_{}'

tmp_path = os.path.join(top_dir, "temp", "temp_bigq_download")


def update_base_lists():
    """update lists derived for BiqQuery
    """
    bigq = bqtools.BigQuery()
    queries = []
    path_map = {}
    print("Building queries")
    for fl in filter_lists:
        sql_path = os.path.join(this_dir, "sql", "{}.sql".format(fl.sql))
        sql = open(sql_path).read()
        # Create a query object for each date range so that we can
        # run all ranges in parallel to speed things up
        for date_range in fl.date_ranges:
            start_date, end_date = date_range
            year = end_date[:4]
            query = sql.format(start_date=start_date, end_date=end_date, **config)
            gcs_path = gcs_path_template.format(len(path_map))
            path_map[gcs_path] = (fl.path, year)
            queries.append(dict(
                proj_id=proj_id,
                query=query,
                format="CSV",
                compression="NONE",
                path=gcs_path))
    # As each query finishes, copy the query to local temp dir
    # and then move all but the first line (the header) to
    # its final destination.
    print("Waiting for results:")
    for gcs_path in bigq.parallel_query_and_extract(queries):
        (fl_path, year) = path_map[gcs_path]
        bqtools.gs_mv(gcs_path, tmp_path)
        dest_path = os.path.join(asset_dir, fl_path, "{}.txt".format(year))
        copy_to_sorted_mmsi(tmp_path, dest_path)
        print("    {0}/{1} done".format(fl_path, year))
    os.unlink(tmp_path)
        
# TODO: should pull from same source as mussidae   
fishing_classes = {  'drifting_longlines',
                     'other_fishing',
                     'pole_and_line',
                     'pots_and_traps',
                     'purse_seines',
                     'set_gillnets',
                     'set_longlines',
                     'squid_jigger',
                     'trawlers',
                     'trollers',
                     'unknown_longline'}


non_fishing_classes = {  'cargo',
                         'motor_passenger',
                         'other_not_fishing',
                         'passenger',
                         'reefer',
                         'sailing',
                         'seismic_vessel',
                         'tanker',
                         'tug'}

def update_derived_lists():
    """Update lists created from base lists
    """
    # Update KNOWN_FISHING list
    infopath = "GFW/VESSEL_INFO/CONSOLIDATED_LISTS.csv"
    path = "GFW/FISHING_MMSI/KNOWN"
    print("Updating", path)
    with open(os.path.join(asset_dir, infopath)) as fin:
        with open(os.path.join(asset_dir, path, "ALL_YEARS.txt"), 'w') as fout:
            reader = csv.DictReader(fin)
            for row in reader:
                if row['label'] in fishing_classes:
                    mmsi = row['mmsi'].strip()
                    fout.write(mmsi + '\n')


    # Update KNOWN_NONFISHING list
    infopath = "GFW/VESSEL_INFO/CONSOLIDATED_LISTS.csv"
    path = "GFW/NONFISHING_MMSI/KNOWN"
    print("Updating", path)
    with open(os.path.join(asset_dir, infopath)) as fin:
        with open(os.path.join(asset_dir, path, "ALL_YEARS.txt"), 'w') as fout:
            reader = csv.DictReader(fin)
            for row in reader:
                if row['label'] in non_fishing_classes:
                    mmsi = row['mmsi'].strip()
                    fout.write(mmsi + '\n')


    # Update combined fishing list
    path = "GFW/FISHING_MMSI/KNOWN_AND_LIKELY"
    print("Updating", path)
    for date_range in default_date_ranges:
            start_date, end_date = date_range
            year = end_date[:4]
            print(year)
            combined = build_combined_fishing_list(asset_dir, year)
            dest_path = os.path.join(asset_dir, path, "{}.txt".format(year))
            with open(dest_path, "w") as dest:
                for mmsi in combined:
                    dest.write(mmsi + '\n')


    



if __name__ == "__main__":
    update_base_lists()
    update_derived_lists()

