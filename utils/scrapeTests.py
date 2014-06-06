#! /usr/bin/env python



'''
Traverses directory and creates json file
'''

import os
import re


TEST_DIR = os.getenv('TEST_DIR', '/Users/Edwin/github/mozilla-b2g/gaia')
FILTER = 'test_.*.(js|py)'
r = re.compile(FILTER)

def scrape_tests(path=TEST_DIR, mintime=0):
    test_files = []
    for dirpath, subdirs, files in os.walk(path):
        for x in files:
            if r.match(x):
                full_path = os.path.join(dirpath, x)
                mod_time = int(os.stat(full_path).st_mtime)
                if mod_time > mintime:
                    test_files.append({'test':full_path, 'mod_time':mod_time})

    return test_files


if __name__ == '__main__':
    print scrape_tests(mintime=1402077088)