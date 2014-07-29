#! /usr/bin/env python

'''
Traverses directory and creates json file
'''

import os
import re
from sqlalchemy import *
import configparser
from sqlalchemy.orm import sessionmaker
import sys
sys.path.append("..")
from db.models import TestCases, Manis, Cats, CatLink

DB_NAME = 'tmi_db'
TEST_DIR = os.getenv('TEST_DIR', '/Users/Edwin/github/mozilla-b2g/gaia')
# IGNORE_DIR = ['ENV', 'node_modules']
engine = create_engine('mysql://dbuser:dbuser@localhost/%s' % DB_NAME)
conn = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()

def read_mani(mani_path):
    mani = configparser.ConfigParser()
    mani._interpolation = configparser.ExtendedInterpolation()
    mani.read(mani_path)
    return mani._sections

def scrape_tests(path=TEST_DIR, mintime=0):
    test_files = []
    mani_files = []
    test_filter = re.compile('test_.*.(js|py)$')
    for dirpath, subdirs, files in os.walk(path):
        # if dirpath.find('ENV') or dirpath.find('node_modules'):
        if dirpath.find('node_modules') > 0:
            continue
        if dirpath.find('ENV') > 0:
            continue
        for x in files:
            if x == 'manifest.ini':
                full_path = os.path.join(dirpath, x)
                mod_time = int(os.stat(full_path).st_mtime)
                mani_files.append({'path':full_path[len(path)+1:],'mod_time':mod_time})
            if test_filter.match(x):
                full_path = os.path.join(dirpath, x)
                mod_time = int(os.stat(full_path).st_mtime)
                if mod_time > mintime:
                    test_files.append({'path':full_path[len(path)+1:], 'mod_time':mod_time})

    return mani_files, test_files

def insert_test_data(tests):
    add_tests = []
    for test in tests:
        add_tests.append(TestCases(test['path'], test['mod_time']))
    session.add_all(add_tests)
    session.commit()

def insert_mani_data(mani_files):
    add_manis = []
    for mani in mani_files:
        add_manis.append(Manis(mani['path'], mani['mod_time']))
    session.add_all(add_manis)
    session.commit()

def insert_cat_link(cat_link_json):
    print 'insert cat', cat_link_json
    # trans = conn.begin()
    # conn.execute(cat_link.insert(), cat_link_json)
    # trans.commit()

def get_or_create_cat(category):
    cat = session.query(Cats).filter(Cats.desc == category)
    cat_id = cat.first()
    if not(cat_id):
        add_cat = Cats(category)
        session.add(add_cat)
        session.flush()
        cat_id = add_cat.id
    return cat_id

def sync_mani(manis):
    # get test ID
    for mani_file in manis:
        mani_dict = read_mani(os.path.join(TEST_DIR, mani_file['path']))
        for test,cats in mani_dict.items():
            if test.startswith('include') or test.startswith('DEFAULT'):
                continue
            test_id = session.query(TestCases).filter(TestCases.path.like('%%%s' % test)).first()
            test_id = test_id.id
            for cat in cats:
                cat_str = "%s %s" % (cat, cats[cat])
                cat_id = get_or_create_cat(cat_str)
                insert_cat_link({'test_id':test_id, 'cat_id':cat_id})

if __name__ == '__main__':
    mani_files, tests_json = scrape_tests()
    # insert_test_data(tests_json)
    # insert_mani_data(mani_files)
    # sync_mani(mani_files)

    # tests_json = scrape_tests()
    # mani_files, tests_json = scrape_tests(mintime=1402077088)
    # f = [{'mod_time': 1396655708, 'path': 'tests/python/gaia-ui-tests/gaiatest/tests/unit/settings/manifest.ini'}]
    # sync_mani(f)

    # m = {"test_settings.py": {}, "test_cell_data_settings.py": {"skip-if": "device == \"desktop\" || device == \"qemu\"", "carrier": "true", "online": "true"}, "test_cell_roaming_settings.py": {"skip-if": "device == \"desktop\"", "carrier": "true"}, "test_wifi_settings.py": {"skip-if": "device == \"desktop\" || device == \"qemu\"", "wifi": "true"}}
    # print get_or_create_cat('abc')
    # print get_or_create_cat('xyz')
    # print read_mani('/Users/Edwin/github/mozilla-b2g/gaia/tests/python/gaia-ui-tests/gaiatest/tests/functional/gallery/manifest.ini')




