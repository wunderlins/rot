import web, config, json, db
import datetime
import time
from sqlalchemy import *
import tpl
import re
import base64

urls = (
  '/', 'personal',
  '/personal(.*)', 'personal',
	'/personal_data', 'personal_data',
	'/test', 'test', # test methods, remove these in production
	'/wunsch', 'wunsch', # test methods, remove these in production
	'/wunsch_save', 'wunsch',
	'/typeahead', 'typeahead',
	'/image(.*)', 'image',
)

def basic_auth():
	allowed = (
		('admin','pass'),
	)
	
	#print web.sess["user"]
	
	auth = web.ctx.env.get('HTTP_AUTHORIZATION')
	if auth is not None:
		web.sess["user"] = None
		auth = re.sub('^Basic ','',auth)
		username,password = base64.decodestring(auth).split(':')
		#print username,password
		if (username,password) in allowed:
			#print "allowd"
			web.sess["user"] = username
			return
	
	if web.sess["user"] == None:
		web.header('WWW-Authenticate','Basic realm="Auth example"')
		web.ctx.status = '401 Unauthorized'
		return

class response:
	
	def __init__(self):
		"""
		Every response object will, when instatiated, do a basic authentication.
		
		This is globally applied for now, that means, there is no way to serve pages to anonymous users.
		
		Not sure if this is a sane way.
		
		"""
		basic_auth()
	
	def header(self, content_type="text/html"):
		web.header('Content-Type', content_type+'; charset=utf-8', unique=True) 
		web.header('Cache-Control','no-cache, no-store, must-revalidate')
		web.header('Pragma','no-cache')
		web.header('Expires','0')
	
	def render(self):
		global urls
		
		return web.template.render('template', base="layout", globals={
			'wunsch_select_wunsch': tpl.wunsch_select_wunsch,
			'wunsch_select_prio': tpl.wunsch_select_prio,
			'wunsch_prio': tpl.wunsch_prio,
			'btn_cancel': tpl.btn_cancel,
			'btn_ok': tpl.btn_ok,
			'urls': urls,
			"session": web.sess
		})

	def person(self, pid, history):
		# get latest wishes
		if history == None:
			w = db.session.query(db.Wunsch).filter_by(pid=pid, latest=1)
		else:
			endd = history + datetime.timedelta(days=1)
			w = db.session.query(db.Wunsch).filter_by(pid=pid).filter(
				and_(db.Wunsch.created >= datetime.date(history.year, history.month, history.day),\
				db.Wunsch.created < datetime.date(endd.year, endd.month, endd.day))
			)
			
		#print u
		g = db.session.query(db.Group).order_by(db.Group.sort)
		
		# modified dates
		d = db.session.query(db.distinct(db.Wunsch.created)).filter_by(pid=pid)
		dates = []
		for dt in d:
			dates.insert(0, dt[0])
		
		wunsch = {}
		for gr in g:
			for r in gr.rot:
				wunsch[r.id] = {"prio": 0, "wunsch": None}
				for e in w:
					if e.rot_id == r.id:
						#print e
						wunsch[r.id] = {"prio": e.prio, "wunsch": e.janein}
						break
		return (g, wunsch, dates)

class test(response):
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
		
		self.header(content_type="application/json")
		return out

class image(response):
	def GET(self, path):
		pid = None
		
		if path:
			#print "Path: " + path
			pid = path[1:]
		#print "pid: " + pid
		
		no_image = False
		try:
			r = db.session.query(db.Person).filter_by(pid=pid)[0]
			web.header("Content-type", "image/jpeg")
			return r.foto
		
		except:
			no_image = True
	
	def POST(self, pid):
		
		personal = db.session.query(db.Personal).filter_by(pid=pid)[0]
		
		if len(personal.rot_pers) == 0:
			p = db.Person()
			p.personal = personal
		else:
			p = personal.rot_pers[0]
		
		f = web.input(file={})
		p.foto = f["file"].value
		
		db.session.commit()
		return ""

class personal_data(response):
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

		self.header(content_type="application/json")
		
		for p in db.session.query(db.Personal).\
			order_by(asc(db.Personal.name)).\
			with_entities(db.Personal.pid, db.Personal.name, db.Personal.vorname, db.Personal.kuerzel).\
			filter_by(aktiv=1, pidp=''):
			ret += json.dumps({"pid": p[0], "name": p[1], "vorname": p[2], "kuerzel": p[3]}, encoding=db.Personal.encoding) + ",\n"
			#ret += str(p.as_json()) + ",\n"
			
		return ret[:-2] + "]"

class typeahead(response):
	def GET(self):
		
		ret = 'var names = { "options": [';
		self.header(content_type="application/json")
		
		for p in db.session.query(db.Personal).\
			order_by(asc(db.Personal.name)).\
			with_entities(db.Personal.pid, db.Personal.name, db.Personal.vorname, db.Personal.kuerzel).\
			filter_by(aktiv=1, pidp=''):
			ret += json.dumps({"pid": p[0], "name": p[1], "vorname": p[2], "kuerzel": p[3], "str": str(p[1]) + " " + str(p[2]) + " (" + str(p[3]) + ")"}, encoding=db.Personal.encoding) + ",\n"
			#ret += str(p.as_json()) + ",\n"
			
		return ret[:-2] + "]}"

class personal(response):
	def GET(self, path=None):
		
		pid = None
		
		if path:
			#print "Path: " + path
			pid = path[1:]
		else:
			return self.render().index(db.Personal(), {})
		
		#print "pid: " + pid
		#web.sess.pid += 1
		#print web.sess.pid
		
		person = db.session.query(db.Personal).filter_by(pid=pid)[0]
		wunsch = db.session.query(db.Wunsch)\
			.filter_by(pid=pid, latest=1)\
			.order_by(db.Wunsch.prio.asc())
		
		global render
		return self.render().index(person, wunsch)
		#return "Hello World"

class wunsch(response):
	def GET(self):
		
		pid = 188 # thierry, change with session pid
		
		history = None
		try:
			h = web.input(name="history").history
			h2 = time.strptime(h, "%d.%m.%Y")
			history = datetime.datetime(h2.tm_year, h2.tm_mon, h2.tm_mday)
		except: pass
		#print history
		
		# get user info
		u = db.session.query(db.Personal).filter_by(pid=pid)[0]
		
		#print u
		
		"""
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
				wunsch[r.id] = {"prio": 0, "wunsch": None}
				for e in w:
					if e.rot_id == r.id:
						#print e
						wunsch[r.id] = {"prio": e.prio, "wunsch": e.janein}
						break
		"""
		
		"""
		render = web.template.render('template', base="layout", globals={
			'wunsch_select_wunsch': tpl.wunsch_select_wunsch,
			'wunsch_select_prio': tpl.wunsch_select_prio,
		})
		"""
		
		(g, wunsch, dates) = self.person(188, history)
		
		global render
		#return render.wunsch(g, u, wunsch, dates, history)
		return self.render().wunsch(g, u, wunsch, dates, history)
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
			
			if wunsch[id]["wunsch"] != "1":
				wunsch[id]["prio"] = 0
			
			w = db.Wunsch()
			w.pid=pid
			w.janein=wunsch[id]["wunsch"]
			w.rot_id=id
			w.prio=wunsch[id]["prio"]
			w.latest = 1
			
			inserts.append(w)
		
		#print inserts
		db.session.add_all(inserts)
		db.session.commit()
