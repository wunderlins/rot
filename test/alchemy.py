#!/usr/bin/env python


import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib', 'SQLAlchemy', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import config

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

# relational features
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

# connect to database
dsn = "mysql+mysqldb://"+config.db_user+":"+config.db_pass+"@localhost/"+config.db_name
#engine = create_engine('sqlite:///:memory:', echo=True)
engine = create_engine(dsn, echo=True)
Base = declarative_base()

# data definitions
"""
class User(Base):
	__tablename__ = 'users'
	
	id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
	name = Column(String(50))
	fullname = Column(String(50))
	password = Column(String(25))
	
	def __repr__(self):
		return "<User(name='%s', fullname='%s', password='%s')>" % (
			self.name, self.fullname, self.password)
"""

## define new tables
class Location(Base):
	__tablename__ = 'rot_location'
	
	id      = Column(Integer, Sequence('location_id_seq'), primary_key=True)
	name    = Column(String(100))
	sort    = Column(Integer)
	deleted = Column(Integer, server_default = "0")


class Cluster(Base):
	__tablename__ = 'rot_cluster'
	
	id      = Column(Integer, Sequence('cluster_id_seq'), primary_key=True)
	name    = Column(String(100))
	sort    = Column(Integer)
	deleted = Column(Integer, server_default = "0")

class Rotation(Base):
	__tablename__ = 'rot_rotation'
	
	id          = Column(Integer, Sequence('rotation_id_seq'), primary_key=True)
	name        = Column(String(100))
	bemerkung   = Column(String(250))
	sort        = Column(Integer)
	dauer_von   = Column(Integer)
	dauer_bis   = Column(Date)
	dauer_step  = Column(Date)
	wunsch      = Column(Integer)
	wunsch_prio = Column(Integer)
	deleted     = Column(Integer, server_default = "0")
	user_id     = Column(Integer, ForeignKey('rot_cluster.id'))
	
	user = relationship("Cluster", backref=backref('rot_rotation', order_by=id))

class Erfahrung(Base):
	__tablename__ = 'rot_erfahrung'
	
	id          = Column(Integer, Sequence('erfahrung_id_seq'), primary_key=True)
	pid         = Column(Integer)
	von         = Column(Date)
	bis         = Column(Date)
	location_id = Column(Integer, ForeignKey('rot_location.id'))
	
	wunsch      = Column(Integer)
	prio        = Column(Integer)
	
	location = relationship("Location", backref=backref('rot_location', order_by=id))

# drop all own tables
Erfahrung.__table__.drop(engine)
Rotation.__table__.drop(engine)
Cluster.__table__.drop(engine)
Location.__table__.drop(engine)

# create tables from scratch
Base.metadata.create_all(engine)

## definition for existing tables
class Personal(Base):
	__tablename__ = 'personal'
	
	pid         = Column(Integer, Sequence('personal_id_seq'), primary_key=True)
	pidp        = Column(Integer)
	personalid  = Column(String(20))
	aktiv       = Column(String(1))
	kuerzel     = Column(String(20))
	ptid        = Column(Integer)
	anrede      = Column(String(20))
	titel       = Column(String(20))
	gebdatum    = Column(Date)
	bemerkung1  = Column(Text)
	bemerkung2  = Column(Text)
	email       = Column(String(50))

# bind engine to a session
Session = sessionmaker(bind=engine)
session = Session()

"""
# create a record and commit it
ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
session.add(ed_user)
"""
session.commit()

"""
# change attribute
ed_user.password = '1234'

# test for uncommited changes
print session.dirty
print session.new

#our_user = session.query(User).filter_by(name='ed').first()
#our_user
"""


