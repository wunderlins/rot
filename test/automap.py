#!/usr/bin/env python

import os, sys, re
sys.path.append(os.path.join('..', 'lib', 'SQLAlchemy', 'lib'))
sys.path.append(os.path.join('..'))

import config
dsn = "mysql+mysqldb://"+config.db_user+":"+config.db_pass+"@localhost/"+config.db_name

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

Base = automap_base()

# engine, suppose it has two tables 'user' and 'address' set up
engine = create_engine(dsn)

# reflect the tables
Base.prepare(engine, reflect=True)

# mapped classes are now created with names by default
# matching that of the table name.
#User = Base.classes.user
#Address = Base.classes.address

Personal = Base.classes.personal

session = Session(engine)

# rudimentary relationships are produced
#session.add(Address(email_address="foo@bar.com", user=User(name="foo")))
#session.commit()

# collection-based relationships are by default named
# "<classname>_collection"
print (Personal)