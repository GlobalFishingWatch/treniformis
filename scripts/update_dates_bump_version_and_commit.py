import os
import yaml
import datetime
import logging
from utility import this_dir
import subprocess
from update_all import update_all

logging.getLogger().setLevel('INFO')

INITIAL_YEAR = 2012
LAG = 3


def update_config():
    config_path = os.path.join(this_dir, 'update_filter_lists_config.yml')
    with open(config_path) as f:
        config = yaml.load(f)
    today = datetime.date.today()
    last_valid_day = today - datetime.timedelta(days=LAG)

    logging.info('Generating new date ranges:')
    date_ranges = []
    year = INITIAL_YEAR
    while year <= last_valid_day.year:
        if year < last_valid_day.year:
            rng = ['{}-01-01'.format(year), '{}-12-31'.format(year)]
        else:
            # These ranges are inclusive so useing a full year gives 366 days
            first_day = last_valid_day - datetime.timedelta(days=364)
            start = '{d.year}-{d.month}-{d.year}'.format(d=first_day)
            end = '{d.year}-{d.month:02}-{d.day:02}'.format(d=last_valid_day)
            rng = [start, end]
        logging.info('\t%s', rng)
        date_ranges.append(rng)
        year += 1

    made_changes = (date_ranges != config['default_date_ranges'])
    if not made_changes:
        logging.info('Config unchanged')

    if made_changes:
        config['default_date_ranges'] = date_ranges
    with open(config_path, 'w') as f:
        yaml.dump(config, f)

    return end if made_changes else False


def bump_minor_version_number():
    version_path = os.path.join(this_dir, '../VERSION')
    with open(version_path) as f:
        version_string = f.read().strip()
    parts = version_string.split('.')
    assert len(parts) <= 3, 'too many parts to version string'

    # Default major, minor, subversions to 0
    parts = (parts + ['0', '0', '0'])[:3]
    version = [int(x.strip()) for x in parts]

    # Bump the version number
    version[2] += 1

    new_version_string = '.'.join(str(x) for x in version)
    # Store back
    with open(version_path, 'w') as f:
        f.write(new_version_string)

    return new_version_string



if __name__ == '__main__':
    new_end_date = update_config()
    if not new_end_date:
        print('No changes since last update, exiting')
        raise SystemExit()
    print('Updated "update_filter_lists_config.yml"')

    print('Updating Lists')
    update_all()

    new_version = bump_minor_version_number()
    print("Bumped version to `{}`".format(new_version))

    # Make sure we are actually in git tree!
    os.chdir(this_dir)

    # Commit changes
    subprocess.call(['git', 'add', '-u'])
    subprocess.call(['git', 'commit' '-m', 'update to {}'.format(new_version)])
    print("Committed changes")

    # Tag release
    subprocess.call(['git', 'tag', '-a', new_version, '-m', 'Update lists through {}'.format(new_end_date)])
    subprocess.call(['git', 'push', 'origin', new_version])
    print("Tagged and pushed release")

