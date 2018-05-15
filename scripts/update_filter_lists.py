from __future__ import print_function
import bqtools
import glob
import treniformis
import os
import six
import csv
from utility import this_dir
from utility import top_dir
from utility import asset_dir
from utility import default_date_ranges
from utility import filter_lists, filter_lists_2
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
    known_nonfishing_path = 'GFW/NONFISHING_MMSI/KNOWN/ALL_YEARS.txt'
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
        


def update_mappings():
    """update lists derived for BiqQuery
    """
    bigq = bqtools.BigQuery()
    queries = []
    path_map = {}
    print("Building queries")
    for fl in filter_lists_2:
        sql_path = os.path.join(this_dir, "sql", "{}.sql".format(fl.sql))
        sql = open(sql_path).read()
        # Create a query object for each date range so that we can
        # run all ranges in parallel to speed things up
        query = sql.format(**config)
        gcs_path = gcs_path_template.format(len(path_map))
        path_map[gcs_path] = fl.path
        queries.append(dict(
            proj_id=proj_id,
            query=query,
            format="CSV",
            compression="NONE",
            path=gcs_path,
            use_legacy_sql=False))
    # As each query finishes, copy the query to local temp dir
    # and then move all but the first line (the header) to
    # its final destination.
    print("Waiting for results:")
    for gcs_path in bigq.parallel_query_and_extract(queries):
        fl_path = path_map[gcs_path]
        bqtools.gs_mv(gcs_path, tmp_path)
        dest_path = os.path.join(asset_dir, fl_path)
        copy_to_sorted_mmsi(tmp_path, dest_path)
        print("    {0} done".format(fl_path))
    os.unlink(tmp_path)


# TODO: should pull from same source as mussidae   
fishing_classes = {  'drifting_longlines',
                     'fixed_gear',
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
                         'cargo_or_tanker',
                         'motor_passenger',
                         'other_not_fishing',
                         'passenger',
                         'reefer',
                         'sailing',
                         'seismic_vessel',
                         'tanker',
                         'tug',
                         'gear'}

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
    any_year = set()
    for date_range in default_date_ranges:
            start_date, end_date = date_range
            year = end_date[:4]
            print(year)
            combined = build_combined_fishing_list(asset_dir, year)
            any_year |= set(combined)
            dest_path = os.path.join(asset_dir, path, "{}.txt".format(year))
            with open(dest_path, "w") as dest:
                for mmsi in combined:
                    dest.write(mmsi + '\n')
    dest_path = os.path.join(asset_dir, path, "ANY_YEAR.txt")
    with open(dest_path, "w") as dest:
        for mmsi in sorted(any_year):
            dest.write(mmsi + '\n')

    # Update suspected fishing list
    path = "GFW/FISHING_MMSI/SUSPECTED/ANY_YEAR.txt"
    print("Updating", path)
    joint = set(any_year)
    with open(os.path.join(asset_dir, "GFW/VESSEL_INFO/VESSEL_LISTS/ALL_YEARS.csv")) as fin:
        with open(os.path.join(asset_dir, path), 'w') as fout:
            reader = csv.DictReader(fin)
            for row in reader:
                label = row['inferred']
                if label in fishing_classes:
                    mmsi = row['mmsi'].strip()
                    joint.add(mmsi)
                    fout.write(mmsi + '\n')
                else:
                    assert label in non_fishing_classes, "{} not in non-fishing".format(label)

    # Update joint fishing list
    path = "GFW/FISHING_MMSI/KNOWN_LIKELY_AND_SUSPECTED/ANY_YEAR.txt"
    print("Updating", path)
    any_year = set()
    with open(os.path.join(asset_dir, path), 'w') as fout:
        for mmsi in sorted(joint):
            fout.write(str(mmsi) + '\n')


def update_fishing_vessel_lists():
    # Update fishing vessel lists based on vessel lists
    base_path = "GFW/VESSEL_INFO/VESSEL_LISTS"
    for in_path in glob.glob(os.path.join(asset_dir, base_path, "LABELS_????.csv")):
        year = os.path.splitext(in_path)[0].rsplit('_', 1)[1]
        out_path = os.path.join(os.path.join(asset_dir, base_path, "FISHING_LABELS_{}.csv".format(year)))
        with open(in_path) as fin:
            with open(out_path, 'w') as fout:
                reader = csv.DictReader(fin)
                writer = None
                for row in reader:
                    label = row['inferred']
                    if label in fishing_classes:
                        if writer is None:
                            writer = csv.DictWriter(fout, reader.fieldnames)
                            writer.writeheader()
                        writer.writerow(row)
                    else:
                        assert label in non_fishing_classes, "{} not in non-fishing".format(label)

mapped_list_globs = [
    "GFW/ACTIVE_MMSI/*.txt",
    "GFW/FISHING_MMSI/*/*.txt",
    "GFW/SPOOFING_MMSI/*.txt",
    "GFW/NONFISHING_MMSI/*.txt"
]


def update_mapped_lists():
    mappath = os.path.join(asset_dir, 'GFW/ID_MAPS/mmsi-to-vessel-id.csv')
    with open(mappath) as f:
        mmsi_ids = [x.split(',') for x in f.read().strip().split()]
    idmap = dict(mmsi_ids)
    # Update lists by mapping mmsi to vessel_id
    for inglob in mapped_list_globs:
        for inpath in glob.glob(os.path.join(asset_dir, inglob)):
            items = []
            outpath = inpath.replace('_MMSI/', '_VESSEL_IDS/')
            print("Updating {} from {}".format(outpath, inpath))
            with open(inpath) as source:
                items = [idmap[x] for x in source.read().strip().split()]
                items.sort()
            with open(outpath, 'w') as sink:
                for x in items:
                    sink.write(x + '\n')



if __name__ == "__main__":
    # update_mappings()
    # update_base_lists()
    # update_derived_lists()
    # update_fishing_vessel_lists()
    update_mapped_lists()

