#!/usr/bin/env python


import os, sys, re
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
engine = create_engine(dsn, echo=False)

# reflect the tables
Base.prepare(engine, reflect=True)

"""
for table in Base.classes.values():
	print " ""class %s(Base):
	__table__ = Table(%r, Base.metadata, autoload=True)
" "" % (table.__name__, table.__name__)
"""

baseclass = "Base, SerializeJson"
def tp(s):
	s = s.replace("VARCHAR", "STRING")
	# replace everything after the first space
	s = re.sub(" .*", "", s)
	return s

for e in Base.metadata.tables.values():
	
	if str(e.name)[0:4] == "rot_":
		continue
	
	print "\nclass %s(%s):" % (e.name, baseclass)
	
	for c in e.columns:
		t = tp(str(c.type))
		sys.stdout.write("\t%s = Column(%s" % (c.name, t[0:1] + t[1:].lower()))
		
		if c.primary_key:
			sys.stdout.write(", primary_key=True")
		
		if c.server_default:
			sys.stdout.write(", server_default=" + c.server_default.arg.text)

		print ")"


