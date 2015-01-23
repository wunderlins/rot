#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib', 'web'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
#sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
#sys.path.append(os.path.join('sw', 'lib', 'python2.7', 'site-packages'))

print sys.path

import web, config, json
from db import * 
from sqlalchemy import *

from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

dsn = "mysql+mysqldb://"+config.db_user+":"+config.db_pass+"@localhost/"+config.db_name + "?charset=utf8"
#engine = create_engine('sqlite:///:memory:', echo=True)
engine = create_engine(dsn, encoding='utf-8', echo=config.db_debug)

Base = declarative_base()


Session = sessionmaker(bind=engine)
session = Session()


#if __name__ == "__main__":
	
session.add_all([
	Location(name="USB", sort=1),
	Location(name="UKBB", sort=2),
	Location(name="Liestal", sort=3),
	Location(name="Olten", sort=4),
	Location(name="Solothurn", sort=5),
	Location(name="Kinderspital Zürich", sort=5),
])
session.commit()

session.add_all([
	Group(name="Viszeral/Urologie/Lunge", sort=1),
	Group(name="Kiefer/HNO", sort=2),
	Group(name="Herz/Gefäss", sort=3),
	Group(name="OP-West", sort=4),
	Group(name="Notfallmedizin/Traumatologie", sort=5),
	Group(name="Weisse Zone", sort=6),
	Group(name="Schmerz", sort=7),
	Group(name="Intensivmedizin", sort=8),
	Group(name="Kinderanästhesie", sort=9)
])
session.commit()

def make_rot(name, bemerk, sort, dauer_von, dauer_bis, group, location, dauer_step=1, erstjahr=0):
	return Rot(name=name, bemerkung=bemerk, sort=sort, dauer_von=dauer_von, dauer_bis=dauer_bis, dauer_step=dauer_step, 
		group=session.query(Group).filter(Group.name==group)[0], 
		location=session.query(Location).filter(Location.name==location)[0],
		erstjahr=erstjahr)

session.add_all([
	make_rot('Allgemeinchirurgie, Urologie', '', 1, 3, 12, "Viszeral/Urologie/Lunge", "USB", 1, 1),
	make_rot('Thorax-Lunge',                 '', 2, 3,  3, "Viszeral/Urologie/Lunge", "USB"),

	make_rot('Kiefer', '', 1, 3,  3, "Kiefer/HNO", "USB", 1, 1),
	make_rot('HNO', '', 2, 3,  3, "Kiefer/HNO", "USB", 1, 1),

	make_rot('Herz/Gefäss',                  '', 1, 4,  4, "Herz/Gefäss", "USB"),

	make_rot('Gyn/Geb. ab 2. AA Jahr', '', 1, 12,  12, "OP-West", "USB"),
	make_rot('Gyn/Geb. ab 4. AA Jahr', '', 2, 6,  6, "OP-West", "USB"),
	make_rot('Neuro',                 '', 3, 4,  4, "OP-West", "USB"),
	make_rot('Orthopädie/Plast. Chirurgie', '', 4, 3,  3, "OP-West", "USB", 1, 1),

	make_rot('Notfallrotation kurz', 'beinhaltet Dienst & Notarzt bei Sanität BS', 1, 3,  3, "Notfallmedizin/Traumatologie", "USB"),
	make_rot('Traumatologie', '', 2, 3,  3, "Notfallmedizin/Traumatologie", "USB", 1, 1),
	make_rot('Notfallmedizin SGNOR', 'wird anerkannt als „3 Monate Notfallstation“ für den FA Notarzt; Verlängerungen mit Zusatzausbildung bei Interesse und Eignung nach Absprache möglich', 3, 4,  4, "Notfallmedizin/Traumatologie", "USB"),
	make_rot('REGA',                 '', 4, 8,  8, "Notfallmedizin/Traumatologie", "USB"),

	make_rot('Augenspital', '', 1, 3,  3, "Weisse Zone", "USB", 1, 1),
	make_rot('PAS', '', 2, 1,  3, "Weisse Zone", "USB", 1, 1),
	
	make_rot('Chronic Pain',                 '', 1, 6,  12, "Schmerz", "USB", 6),
	
	make_rot('OIB',                 '', 1, 6,  24, "Intensivmedizin", "USB"),
	make_rot('Austausch MIPS',                 '', 2, 6,  6, "Intensivmedizin", "USB"),

	make_rot('UKBB Kinderanästhesie',                 '', 1, 4,  12, "Kinderanästhesie", "UKBB", 8),
	make_rot('Kinderspital Zürich',                 '', 2, 12,  12, "Kinderanästhesie", "Kinderspital Zürich"),
])

session.commit()


"""
	id          = Column(Integer, Sequence('rot_id_seq'), primary_key=True)
	name        = Column(String(100))
	bemerkung   = Column(String(250))
	sort        = Column(Integer)
	dauer_von   = Column(Integer)
	dauer_bis   = Column(Integer)
	dauer_step  = Column(Integer)
	#wunsch      = Column(Integer)
	#wunsch_prio = Column(Integer)
	
	group_id    = Column(Integer, ForeignKey('rot_group.id'))
	location_id = Column(Integer, ForeignKey('rot_location.id'))
"""
