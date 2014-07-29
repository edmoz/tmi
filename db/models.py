

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import scoped_session, sessionmaker


Base = declarative_base()
DB_NAME = 'tmi_db'
CONN_STR = 'mysql://dbuser:dbuser@localhost/%s' % DB_NAME

Session = scoped_session(sessionmaker())

CatLink = Table('tmi_cat_link', Base.metadata,
    Column('test_id', Integer, ForeignKey('tmi_tests.id')),
    Column('cat_id', Integer, ForeignKey('tmi_cats.id'))
)
# class CatLink(Base):
#     """"""
#     __tablename__ = "tmi_cat_link"

#     test_id = Column(Integer, ForeignKey('tmi_tests.id'), primary_key=True)
#     cat_id = Column(Integer, ForeignKey('tmi_cats.id'), primary_key=True)

#     def __init__(self, test_id, cat_id):
#         """"""
#         self.test_id = test_id
#         self.cat_id = cat_id

class TestCases(Base):
    """"""
    __tablename__ = "tmi_tests"
    # __table_args__ = {"useexisting": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    path = Column(VARCHAR(255), nullable=False)
    mod_time = Column(Integer, nullable=False)
    cats = relationship("Cats", secondary=CatLink)

    def _find_or_create_cat(self, cat):
        q = Cats.query.filter_by(desc=cat)
        t = q.first()
        if not(t):
            t = Cats(cat)
        return t

    def _get_cats(self):
        return [x.name for x in self.cats]

    def _set_cats(self, value):
        self.cats.append(self._find_or_create_cat(value))

    str_cats = property(_get_cats,
                        _set_cats,
                        "Property str_cats is a simple wrapper for cats relation")

    def __init__(self, path, mod_time):
        """"""
        self.path = path
        self.mod_time = mod_time

class Cats(Base):
    """"""
    __tablename__ = "tmi_cats"
    query = Session.query_property()

    id = Column(Integer, primary_key=True, autoincrement=True)
    desc = Column(VARCHAR(255), nullable=False)
    name = Column(VARCHAR(255), nullable=True)
    testCases = relationship("TestCases", secondary=CatLink)

    def __init__(self, desc, name=""):
        """"""
        self.desc = desc
        self.name = name

class Manis(Base):
    """"""
    __tablename__ = "tmi_mani"

    id = Column(Integer, primary_key=True, autoincrement=True)
    path = Column(VARCHAR(255), nullable=False)
    mod_time = Column(Integer, nullable=False)

    def __init__(self, path, mod_time):
        """"""
        self.path = path
        self.mod_time = mod_time 




def create_db(engine):
    Base.metadata.create_all(engine)

def db_connect():
    return create_engine(CONN_STR)

engine = db_connect()
create_db(engine)
