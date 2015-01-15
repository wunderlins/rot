#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Start application server on port 8080

The first command line argument will set the port to be bound. Remeber, you 
need root privvileges to bind ports below 1024.

"""

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib', 'web'))

import web, config, json, db
import datetime
import time
from sqlalchemy import *

# allow to pass a custom port/ip into the application
class rot(web.application):
	def run(self, port=8080, ip='0.0.0.0', *middleware):
		func = self.wsgifunc(*middleware)
		return web.httpserver.runsimple(func, (ip, port))

urls = (
  '/', 'index',
	'/personal', 'personal',
	'/test', 'test', # test methods, remove these in production
	'/wunsch', 'wunsch', # test methods, remove these in production
	'/wunsch_save', 'wunsch'
)

class test:
	def GET(self):
		s = db.session
		#p = s.query(db.personal).filter_by(aktiv=1)
		out = ""
		for r in s.query(db.Personal).filter_by(aktiv=1):
			#print r
			#out += json.dumps(r.as_dict(), encoding="8859")
			out += str(r.as_json())
			#out += json.dumps(r, cls=db.AlchemyEncoder)
			#out += r.name + " "
			#out += ":".join("{:02x}".format(ord(c)) for c in r.name)
			out += "\n"
			#out += r.as_dict() + "\n"
		return out

class personal:
	def GET(self):
		"""
		db = web.database(
			host = config.db_host,
			dbn  = 'mysql',
			user = config.db_user,
			pw   = config.db_pass,
			db   = config.db_name
		)
		personal = db.select('personal', what='pid,pidp,kuerzel,name,vorname,ptid,email')
		"""
		ret = "[";
		"""
		for p in personal:
			ret += json.dumps(p) + ",\n"
		ret = "[" + ret[:-2] + "]"
		"""
		for p in db.session.query(db.Personal).\
			order_by(asc(db.Personal.name)).\
			with_entities(db.Personal.pid, db.Personal.name, db.Personal.vorname, db.Personal.kuerzel).\
			filter_by(aktiv=1, pidp=''):
			ret += json.dumps({"pid": p[0], "name": p[1], "vorname": p[2], "kuerzel": p[3]}, encoding=db.Personal.encoding) + ",\n"
			#ret += str(p.as_json()) + ",\n"
			
		return ret[:-2] + "]"

class index:
	def GET(self):
		db = web.database(
			host = config.db_host,
			dbn  = 'mysql',
			user = config.db_user,
			pw   = config.db_pass,
			db   = config.db_name
		)
		#personal = db.select('personal', what='pid,pidp,kuerzel,name,vorname,ptid,email')
		#ret = "";
		#for p in personal:
		#	ret += json.dumps(p) + ",\n"
		#ret = "[" + ret + "]"
		render = web.template.render('template')
		return render.index(None)
		#return "Hello World"

class wunsch:
	def GET(self):
		history = None
		try:
			h = web.input(name="history").history
			h2 = time.strptime(h, "%d.%m.%Y")
			history = datetime.datetime(h2.tm_year, h2.tm_mon, h2.tm_mday)
		except: pass
		print history
		
		# get user info
		u = db.session.query(db.Personal).filter_by(pid='188')[0] # Thierry
		
		# get latest wishes
		if history == None:
			w = db.session.query(db.Wunsch).filter_by(pid='188', latest=1)
		else:
			endd = history + datetime.timedelta(days=1)
			w = db.session.query(db.Wunsch).filter_by(pid='188').filter(
				and_(db.Wunsch.created >= datetime.date(history.year, history.month, history.day),\
				db.Wunsch.created < datetime.date(endd.year, endd.month, endd.day))
			)
		
		#print u
		
		#print u
		g = db.session.query(db.Group).order_by(db.Group.sort)
		
		# modified dates
		d = db.session.query(db.distinct(db.Wunsch.created)).filter_by(pid=188)
		dates = []
		for dt in d:
			dates.insert(0, dt[0])
		
		wunsch = {}
		for gr in g:
			for r in gr.rot:
				wunsch[r.id] = {"prio": 3, "wunsch": None}
				for e in w:
					if e.rot_id == r.id:
						#print e
						wunsch[r.id] = {"prio": e.prio, "wunsch": e.janein}
						break
		
		render = web.template.render('template')
		return render.wunsch(g, u, wunsch, dates, history)
		#return "Hello World"
	
	def POST(self):
		"""
		Colelct user input of wunsch. Store it as active set for user with "pid". 
		If there is already a set with the current day, replace it, otherwise 
		create a new set and make it active.
		"""
		
		#get personalid
		pid = web.input("pid").pid
		#print "PID:", pid
		
		# create name/value pairs for wunsch and prio		
		wunsch = {}		
		for name in web.input():
			if name == "pid": # skip pid
				continue
			
			value = web.input()[name]
			if value == "": # skip unset values
				continue
			
			id = None
			type = ""
			
			# check type
			if name[0:4] == "prio":
				type = "prio"
				id = int(name[5:])
				
			if name[0:6] == "wunsch":
				type = "wunsch"
				id = int(name[7:])
			
			#print type, id, value
			
			try:
				wunsch[id][type] = value
			except:
				wunsch[id] = {"prio": 3, "wunsch": None}
				wunsch[id][type] = value
		
		#print wunsch
		
		# TODO: delete all latest flags
		lw = db.session.query(db.Wunsch).filter_by(pid=pid, latest=1)
		for l in lw:
			l.latest = 0
		db.session.commit()
		
		# get rid of records with the current date
		dt = datetime.datetime.now()
		lw = db.session.query(db.Wunsch).filter(db.Wunsch.created >= datetime.date(dt.year, dt.month, dt.day))
		for l in lw:
			db.session.delete(l)
		db.session.commit()
		
		# insert
		inserts = []
		for id in wunsch.keys():
			
			if wunsch[id]["wunsch"] == None:
				continue
			
			w = db.Wunsch()
			w.pid=pid
			w.janein=wunsch[id]["wunsch"]
			w.rot_id=id
			w.prio=wunsch[id]["prio"]
			w.latest = 1
			
			inserts.append(w)
		
		print inserts
		db.session.add_all(inserts)
		db.session.commit()

import sys, logging
from wsgilog import WsgiLog
import config

class Log(WsgiLog):
	def __init__(self, application):
		WsgiLog.__init__(
									 self,
									 application,
									 logformat = '%(message)s',
									 tofile = True,
									 toprint = True,
									 file = config.app_logfile,
									 #interval = config.log_interval,
									 #backups = config.log_backups
									 )

if __name__ == "__main__":

	# redirect webserver logs to file
	#weblog = open(config.web_logfile, "ab")
	#sys.stderr = weblog
	#sys.stdout = weblog
	
	app = rot(urls, globals())
	app.run(config.port, "0.0.0.0", Log)
