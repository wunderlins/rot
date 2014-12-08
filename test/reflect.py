#!/usr/bin/env python


import os, sys
sys.path.append(os.path.join('..', 'lib', 'SQLAlchemy', 'lib'))
sys.path.append(os.path.join('..'))

import config

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

Base = automap_base()

# connect to database
dsn = "mysql+mysqldb://"+config.db_user+":"+config.db_pass+"@localhost/"+config.db_name
#engine = create_engine('sqlite:///:memory:', echo=True)
engine = create_engine(dsn, echo=True)

# reflect the tables
Base.prepare(engine, reflect=True)

for table in Base.classes.values():
	print """class %s(Base):
	__table__ = Table(%r, Base.metadata, autoload=True)
""" % (table.__name__, table.__name__)