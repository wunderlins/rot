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

from sqlalchemy.ext.declarative import AbstractConcreteBase

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

"""
class Serializable(AbstractConcreteBase, Base):
	#def __init__(self, *args, **kwargs):
	#	super(Serializable, self).__init__(*args, **kwargs)
	
	def as_dict(self):
		return {c.name: getattr(self, c.name) for c in self.__table__.columns}
"""

from sqlalchemy.ext.declarative import declared_attr
class SerializeJson(object):
	def as_dict(self):
		return {c.name: getattr(self, c.name) for c in self.__table__.columns}



## define new tables
class Location(Base, SerializeJson):
	__tablename__ = 'rot_location'
	
	id      = Column(Integer, Sequence('location_id_seq'), primary_key=True)
	name    = Column(String(100))
	sort    = Column(Integer)
	deleted = Column(Integer, server_default = "0")

class Cluster(Base, SerializeJson):
	__tablename__ = 'rot_cluster'
	
	id      = Column(Integer, Sequence('cluster_id_seq'), primary_key=True)
	name    = Column(String(100))
	sort    = Column(Integer)
	deleted = Column(Integer, server_default = "0")

class Rotation(Base, SerializeJson):
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
	cluster_id  = Column(Integer, ForeignKey('rot_cluster.id'))
	
	cluster = relationship("Cluster", backref=backref('rotation', order_by=id))

class Einteilung(Base, SerializeJson):
	__tablename__ = 'rot_erfahrung'
	
	id          = Column(Integer, Sequence('erfahrung_id_seq'), primary_key=True)
	pid         = Column(Integer)
	von         = Column(Date)
	bis         = Column(Date)
	location_id = Column(Integer, ForeignKey('rot_location.id'))
	rotation_id = Column(Integer, ForeignKey('rot_rotation.id'))
	
	wunsch      = Column(Integer)
	prio        = Column(Integer)
	
	confirmed   = Column(Boolean, server_default="1")
	
	rotation    = relationship("Rotation", backref=backref('erfahrung', order_by=id))
	location    = relationship("Location", backref=backref('erfahrung', order_by=id))

# create tables from scratch
Base.metadata.create_all(engine)

"""
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

"""

# reflection of existing tables
metadata = MetaData(bind=engine)
class rotationstyp(Base, SerializeJson):
	__table__ = Table('rotationstyp', metadata, autoload=True)

class log(Base, SerializeJson):
	__table__ = Table('log', metadata, autoload=True)

class rotblock(Base, SerializeJson):
	__table__ = Table('rotblock', metadata, autoload=True)

class permission(Base, SerializeJson):
	__table__ = Table('permission', metadata, autoload=True)

class color(Base, SerializeJson):
	__table__ = Table('color', metadata, autoload=True)

class notes(Base, SerializeJson):
	__table__ = Table('notes', metadata, autoload=True)

class module(Base, SerializeJson):
	__table__ = Table('module', metadata, autoload=True)

class personal(Base, SerializeJson):
	__table__ = Table('personal', metadata, autoload=True)

class setting(Base, SerializeJson):
	__table__ = Table('setting', metadata, autoload=True)

class perstyp(Base, SerializeJson):
	__table__ = Table('perstyp', metadata, autoload=True)

class rotationsort(Base, SerializeJson):
	__table__ = Table('rotationsort', metadata, autoload=True)

class action(Base, SerializeJson):
	__table__ = Table('action', metadata, autoload=True)

class rotation(Base, SerializeJson):
	__table__ = Table('rotation', metadata, autoload=True)

class rotation2person(Base, SerializeJson):
	__table__ = Table('rotation2person', metadata, autoload=True)

class user(Base, SerializeJson):
	__table__ = Table('user', metadata, autoload=True)

# add relations to existing database tables
#Rotation.person = relationship("personal", backref=backref('rotation', order_by=id))
Rotation.person = relationship("personal",
															 foreign_keys="personal.pid",
															 primaryjoin="and_(personal.pid==Rotation.id)",
															 backref="rotation")

# bind engine to a session
Session = sessionmaker(bind=engine)
session = Session()

# commit transaction
#session.commit()

"""
# change attribute
ed_user.password = '1234'

# test for uncommited changes
print session.dirty
print session.new

#our_user = session.query(User).filter_by(name='ed').first()
#our_user
"""


