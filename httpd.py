#!/usr/bin/env python

"""
Start application server on port 8080

The first command line argument will set the port to be bound. Remeber, you 
need root privvileges to bind ports below 1024.

"""

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib', 'web'))
#sys.path.append(os.path.join('sw', 'lib', 'python2.7', 'site-packages'))

import web, config, json, db

# allow to pass a custom port/ip into the application
class rot(web.application):
	def run(self, port=8080, ip='0.0.0.0', *middleware):
		func = self.wsgifunc(*middleware)
		return web.httpserver.runsimple(func, (ip, port))

urls = (
  '/', 'index',
	'/personal', 'personal',
	'/test', 'test' # test methods, remove these in production
)

class test:
	def GET(self):
		s = db.session
		#p = s.query(db.personal).filter_by(aktiv=1)
		out = ""
		for r in s.query(db.personal.name, db.personal.vorname).filter_by(aktiv=1):
			print r;
			out += r.as_dict() + "\n"
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
		ret = "";
		"""
		for p in personal:
			ret += json.dumps(p) + ",\n"
		ret = "[" + ret[:-2] + "]"
		"""
		for p in db.session.query(db.personal).filter_by(aktiv=1):
			ret += json.dumps(p.as_dict()) + "\n"
		return ret

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
		
if __name__ == "__main__":
	
	app = rot(urls, globals())
	app.run(port=config.port)
