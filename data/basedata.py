#!/usr/bin/env python

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib', 'web'))
#sys.path.append(os.path.join('sw', 'lib', 'python2.7', 'site-packages'))

import web, config, json, db
from sqlalchemy import *


#if __name__ == "__main__":
	
session.add_all([
	Location(name="USB", sort=1),
	Location(name="UKBB", sort=2),
	Location(name="Liestal", sort=3),
	Location(name="Olten", sort=4),
	Location(name="Solothurn", sort=5),
])
session.commit()

session.add_all([
	Group(name="Viszeral/Urologie/Lunge", sort=1),
	Group(name="Kiefer/HNO", sort=2),
	Group(name="Herz/Gefäss", sort=3),
	Group(name="OP-WEST", sort=4),
	Group(name="Notfallmedizin/Traumatologie", sort=5),
	Group(name="Weisse Zone", sort=6),
	Group(name="Schmerz", sort=7),
	Group(name="Intensivmedizin", sort=8),
	Group(name="Kinderanästhesie", sort=8)
])
session.commit()

session.add_all([
	Rot(name='', bemerkung='', sort=1, dauer_von=, dauer_bis=, dauer_step=1, group_id),
])


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
