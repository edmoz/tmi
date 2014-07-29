from bottle import route, run, view
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
import sys
sys.path.append("..")
from db.models import TestCases

import os

DB_NAME = 'tmi_db'
TEST_DIR = os.getenv('TEST_DIR', '/Users/Edwin/github/mozilla-b2g/gaia')
# IGNORE_DIR = ['ENV', 'node_modules']
engine = create_engine('mysql://dbuser:dbuser@localhost/%s' % DB_NAME)
metadata = MetaData(engine)

Session = sessionmaker(bind=engine)
session = Session()


@route('/')
@view('view/index')
def manage():
    ret_tests = []
    tests = session.query(TestCases).all()
    for test in tests:
        testpath = test.path.split('/')
        cats = []
        if test.cats:
            for cat in test.cats:
                cats.append(cat.name)
        ret_tests.append({"test":testpath[-1:][0],"path":"/".join(testpath[:-1]), "cats":cats})

    return {'tests':ret_tests}



run(host='localhost', port=9090, debug=True, reloader=True)