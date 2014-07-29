from sqlalchemy import *

execfile('models.py')
from sqlalchemy.orm import sessionmaker
engine = db_connect()
Session = sessionmaker(bind=engine)
session = Session()
tests = session.query(TestCases).all()
for test in tests:
    if test.cats:
        for cat in test.cats:
            print cat.name


DROP TABLE IF EXISTS `tmi_cat_link`;
DROP TABLE IF EXISTS `tmi_tests`;
DROP TABLE IF EXISTS `tmi_mani`;
DROP TABLE IF EXISTS `tmi_cats`;



t = TestCases('b',321)
c = Cats('desc1', 'name1')
t.str_cats = c