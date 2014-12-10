#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, json
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
engine = create_engine(dsn, echo=config.db_debug)
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

"""
from sqlalchemy.ext.declarative import DeclarativeMeta
class AlchemyEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj.__class__, DeclarativeMeta):
			# an SQLAlchemy class
			fields = {}
			for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
				data = obj.__getattribute__(field)
				try:
					json.dumps(data) # this will fail on non-encodable values, like other classes
					fields[field] = data
				except TypeError:
					fields[field] = None
			# a json-encodable dict
			return fields
				
		return json.JSONEncoder.default(self, obj)
"""

class SerializeJson(object):
	encoding = "8859"
	def as_dict(self):
		return {c.name: getattr(self, c.name) for c in self.__table__.columns}
	
	def as_json(self):
		return json.dumps(self.as_dict(), encoding=self.encoding)

class DefaultAttributes(SerializeJson):
	encoding = "utf8"
	# fixme: try to ustilize database features for these timestamps. 
	created = Column(DateTime, nullable=False, default=func.now())
	modified = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())


## define new tables
class Location(Base, DefaultAttributes):
	__tablename__ = 'rot_location'
	
	id	    = Column(Integer, Sequence('location_id_seq'), primary_key=True)
	name	  = Column(String(100))
	sort	  = Column(Integer)
	deleted = Column(Integer, server_default = "0")

class Cluster(Base, DefaultAttributes):
	__tablename__ = 'rot_cluster'
	
	id	    = Column(Integer, Sequence('cluster_id_seq'), primary_key=True)
	name	  = Column(String(100))
	sort	  = Column(Integer)
	deleted = Column(Integer, server_default = "0")

class Rot(Base, DefaultAttributes):
	__tablename__ = 'rot_rot'
	
	id          = Column(Integer, Sequence('rot_id_seq'), primary_key=True)
	name        = Column(String(100))
	bemerkung   = Column(String(250))
	sort        = Column(Integer)
	dauer_von   = Column(Integer)
	dauer_bis   = Column(Date)
	dauer_step  = Column(Date)
	wunsch      = Column(Integer)
	wunsch_prio = Column(Integer)
	deleted	    = Column(Integer, server_default = "0")
	cluster_id  = Column(Integer, ForeignKey('rot_cluster.id'))
	location_id = Column(Integer, ForeignKey('rot_location.id'))
	location    = relationship("Location", backref=backref('erfahrung', order_by=id))
	
	cluster = relationship("Cluster", backref=backref('rot', order_by=id))

class Einteilung(Base, DefaultAttributes):
	__tablename__ = 'rot_erfahrung'
	
	id          = Column(Integer, Sequence('erfahrung_id_seq'), primary_key=True)
	pid         = Column(Integer)
	von	        = Column(Date)
	bis         = Column(Date)
	rot_id      = Column(Integer, ForeignKey('rot_rot.id'))
	
	wunsch      = Column(Integer)
	prio        = Column(Integer)
	
	confirmed   = Column(Boolean, server_default="1")
	
	rot         = relationship("Rot", backref=backref('erfahrung', order_by=id))

# create tables from scratch
Base.metadata.create_all(engine)

## existing tables
class Action(Base, SerializeJson):
	__tablename__ = 'action'

	__table_args__ = {}

	#column definitions
	aid = Column('aid', INTEGER(), primary_key=True, nullable=False)
	def_ = Column('def', Integer(), nullable=False)
	mask = Column('mask', INTEGER())
	name = Column('name', VARCHAR(length=50))

	#relation definitions


class Color(Base, SerializeJson):
	__tablename__ = 'color'

	__table_args__ = {}

	#column definitions
	bg = Column('bg', VARCHAR(length=10))
	cid = Column('cid', INTEGER(), primary_key=True, nullable=False)
	comment = Column('comment', VARCHAR(length=255))
	fg = Column('fg', VARCHAR(length=10))

	#relation definitions


class Log(Base, SerializeJson):
	__tablename__ = 'log'

	__table_args__ = {}

	#column definitions
	comment = Column('comment', TEXT())
	filename = Column('filename', VARCHAR(length=50))
	ip = Column('ip', CHAR(length=15))
	lid = Column('lid', INTEGER(), primary_key=True, nullable=False)
	recid = Column('recid', INTEGER())
	recidx = Column('recidx', VARCHAR(length=20))
	recstr = Column('recstr', TEXT())
	tabname = Column('tabname', VARCHAR(length=50))
	tst = Column('tst', TIMESTAMP(), nullable=False)
	uid = Column('uid', VARCHAR(length=20))

	#relation definitions


class Module(Base, SerializeJson):
	__tablename__ = 'module'

	__table_args__ = {}

	#column definitions
	action = Column('action', INTEGER(), nullable=False)
	beschrieb = Column('beschrieb', VARCHAR(length=150))
	mid = Column('mid', INTEGER(), primary_key=True, nullable=False)
	name = Column('name', VARCHAR(length=30))

	#relation definitions


class Note(Base, SerializeJson):
	__tablename__ = 'notes'

	__table_args__ = {}

	#column definitions
	color = Column('color', CHAR(length=10))
	comment = Column('comment', TEXT())
	nid = Column('nid', INTEGER(), primary_key=True, nullable=False)
	pid = Column('pid', INTEGER(), nullable=False)
	ym = Column('ym', CHAR(length=6))

	#relation definitions


class Permission(Base, SerializeJson):
	__tablename__ = 'permission'

	__table_args__ = {}

	#column definitions
	level = Column('level', INTEGER())
	mid = Column('mid', INTEGER())
	prid = Column('prid', INTEGER(), primary_key=True, nullable=False)
	uid = Column('uid', INTEGER())

	#relation definitions


class Personal(Base, SerializeJson):
	__tablename__ = 'personal'

	__table_args__ = {}

	#column definitions
	pid = Column('pid', INTEGER(), primary_key=True, nullable=False)
	adresse = Column('adresse', VARCHAR(length=100))
	aktiv = Column('aktiv', VARCHAR(length=1))
	anrede = Column('anrede', VARCHAR(length=20))
	bemerkung1 = Column('bemerkung1', TEXT())
	bemerkung2 = Column('bemerkung2', TEXT())
	combi = Column('combi', INTEGER())
	email = Column('email', VARCHAR(length=50))
	f1 = Column('f1', VARCHAR(length=20))
	f10 = Column('f10', VARCHAR(length=20))
	f11 = Column('f11', VARCHAR(length=20))
	f2 = Column('f2', VARCHAR(length=20))
	f3 = Column('f3', VARCHAR(length=20))
	f4 = Column('f4', VARCHAR(length=20))
	f5 = Column('f5', VARCHAR(length=20))
	f6 = Column('f6', VARCHAR(length=20))
	f7 = Column('f7', VARCHAR(length=20))
	f8 = Column('f8', VARCHAR(length=20))
	f9 = Column('f9', VARCHAR(length=20))
	fax = Column('fax', VARCHAR(length=15))
	gebdatum = Column('gebdatum', DATE())
	kuerzel = Column('kuerzel', VARCHAR(length=20))
	name = Column('name', VARCHAR(length=40), nullable=False)
	natel = Column('natel', VARCHAR(length=15))
	notarzt = Column('notarzt', VARCHAR(length=1))
	personalid = Column('personalid', VARCHAR(length=20))
	pid = Column('pid', INTEGER(), primary_key=True, nullable=False)
	pidp = Column('pidp', INTEGER(), nullable=False)
	plz = Column('plz', VARCHAR(length=10))
	ptid = Column('ptid', INTEGER(), nullable=False)
	sgnor = Column('sgnor', VARCHAR(length=1))
	tel_g = Column('tel_g', VARCHAR(length=15))
	tel_p = Column('tel_p', VARCHAR(length=15))
	titel = Column('titel', VARCHAR(length=20))
	verfuegbar = Column('verfuegbar', VARCHAR(length=1))
	vorname = Column('vorname', VARCHAR(length=30), nullable=False)
	wohnort = Column('wohnort', VARCHAR(length=30))

	#relation definitions
	def __repr__(self):
		return "<Personal(name='%s', vorname='%s', pid='%d')>" % (
			self.name, self.vorname, self.pid)
	
	"""
	def as_dict(self):
		return {c.name: getattr(self, c.name) for c in self.__table__.columns}
	"""
	
class Perstyp(Base, SerializeJson):
	__tablename__ = 'perstyp'

	__table_args__ = {}

	#column definitions
	kurz = Column('kurz', VARCHAR(length=4))
	lang = Column('lang', VARCHAR(length=20))
	ptid = Column('ptid', INTEGER(), primary_key=True, nullable=False)
	sort = Column('sort', INTEGER())

	#relation definitions


class Rotation(Base, SerializeJson):
	__tablename__ = 'rotation'

	__table_args__ = {}

	#column definitions
	bemerkung1 = Column('bemerkung1', TEXT())
	bemerkung2 = Column('bemerkung2', TEXT())
	bgrad = Column('bgrad', FLOAT())
	bgradj = Column('bgradj', Integer(), nullable=False)
	cid = Column('cid', INTEGER())
	f1 = Column('f1', VARCHAR(length=10))
	f2 = Column('f2', VARCHAR(length=10))
	jm = Column('jm', INTEGER())
	kuerzel = Column('kuerzel', VARCHAR(length=10))
	meldetyp = Column('meldetyp', INTEGER())
	meldung = Column('meldung', INTEGER())
	pid = Column('pid', INTEGER(), nullable=False)
	rbid = Column('rbid', INTEGER(), nullable=False)
	rid = Column('rid', INTEGER(), primary_key=True, nullable=False)
	rort = Column('rort', INTEGER())
	rpos = Column('rpos', INTEGER(), nullable=False)
	rtyp = Column('rtyp', VARCHAR(length=10))
	show = Column('show', VARCHAR(length=1))
	ukbb = Column('ukbb', Integer())

	#relation definitions


class Rotation2person(Base, SerializeJson):
	__tablename__ = 'rotation2person'

	__table_args__ = {}

	#column definitions
	pid = Column('pid', INTEGER(), nullable=False)
	pos = Column('pos', INTEGER(), nullable=False)
	r2pid = Column('r2pid', INTEGER(), primary_key=True, nullable=False)
	rtid = Column('rtid', INTEGER(), nullable=False)
	ym = Column('ym', CHAR(length=6), nullable=False)

	#relation definitions


class Rotationsort(Base, SerializeJson):
	__tablename__ = 'rotationsort'

	__table_args__ = {}

	#column definitions
	anzpos = Column('anzpos', INTEGER())
	kuerzel = Column('kuerzel', VARCHAR(length=20))
	name = Column('name', VARCHAR(length=50))
	roid = Column('roid', INTEGER(), primary_key=True, nullable=False)
	sort = Column('sort', INTEGER())

	#relation definitions


class Rotationstyp(Base, SerializeJson):
	__tablename__ = 'rotationstyp'

	__table_args__ = {}

	#column definitions
	name = Column('name', VARCHAR(length=20))
	pos = Column('pos', INTEGER(), nullable=False)
	roid = Column('roid', INTEGER())
	rtid = Column('rtid', INTEGER(), primary_key=True, nullable=False)
	sort = Column('sort', INTEGER())

	#relation definitions


class Rotblock(Base, SerializeJson):
	__tablename__ = 'rotblock'

	__table_args__ = {}

	#column definitions
	comment = Column('comment', TEXT())
	neueintritt = Column('neueintritt', Integer(), nullable=False)
	pid = Column('pid', INTEGER())
	rbid = Column('rbid', INTEGER(), primary_key=True, nullable=False)
	rbis = Column('rbis', CHAR(length=6))
	rvon = Column('rvon', CHAR(length=6))

	#relation definitions


class Setting(Base, SerializeJson):
	__tablename__ = 'setting'

	__table_args__ = {}

	#column definitions
	name = Column('name', VARCHAR(length=50))
	sid = Column('sid', INTEGER(), primary_key=True, nullable=False)
	uid = Column('uid', INTEGER())
	value = Column('value', TEXT())

	#relation definitions


class User(Base, SerializeJson):
	__tablename__ = 'user'

	__table_args__ = {}

	#column definitions
	aktiv = Column('aktiv', Integer(), nullable=False)
	kuerzel = Column('kuerzel', VARCHAR(length=10))
	login = Column('login', VARCHAR(length=20))
	name = Column('name', VARCHAR(length=50))
	profil = Column('profil', VARCHAR(length=20))
	pw = Column('pw', VARCHAR(length=20))
	tst = Column('tst', TIMESTAMP(), nullable=False)
	uid = Column('uid', INTEGER(), primary_key=True, nullable=False)
	vorname = Column('vorname', VARCHAR(length=50))

	#relation definitions


# add relations to existing database tables
#Rotation.person = relationship("personal", backref=backref('rotation', order_by=id))
Einteilung.person = relationship("Personal",
															 foreign_keys="Einteilung.pid",
															 primaryjoin="and_(Personal.pid==Einteilung.pid)",
															 backref="einteilung")


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

def dump_personal():
	for p in session.query(Personal).all():
		print p



