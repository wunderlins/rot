import web, config, json, db
import datetime
import time
from sqlalchemy import *
import tpl
import re
import base64
import sys
import os

urls = (
  '/', 'index',
  '/personal(.*)', 'personal',
	'/personal_data', 'personal_data',
	'/test', 'test', # test methods, remove these in production
	'/wunsch(.*)', 'wunsch', # test methods, remove these in production
	'/wunsch_save(.*)', 'wunsch',
	'/typeahead', 'typeahead',
	'/image(.*)', 'image',
	'/rotnote(.*)', 'rotnote',
	'/erfahrung(.*)', 'erfahrung'
)

from HTMLParser import HTMLParser

session = None
session_default = {
	"selected_pid": 0,
	"pid": None,
	"user": None
}

def set_session(s):
	global session
	session = s

def get_session():
	global session
	return session

class MLStripper(HTMLParser):
	def __init__(self):
		self.reset()
		self.fed = []
	
	def handle_data(self, d):
		self.fed.append(d)
	
	def get_data(self):
		return ''.join(self.fed)

def strip_tags(html):
	s = MLStripper()
	s.feed(html)
	return s.get_data()

def basic_auth():
	allowed = (
		('admin', 'pass'),
	)
	
	#session = get_session()
	global session
	if session == None:
		session = session_default
	
	print session
	print "session: "
	for e in session:
		print "%s, %s" % (e, session[e])
	
	auth = web.ctx.env.get('HTTP_AUTHORIZATION')
	if auth is not None and session["user"] == None:
		session["user"] = None
		auth = re.sub('^Basic ','',auth)
		username, password = base64.decodestring(auth).split(':')
		#print username,password
		if (username, password) in allowed:
			#print "allowd"
			session["user"] = username
			session["pid"] = 0
			session["selected_pid"] = 0
			return
	
	if session["user"] == None:
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
		print session
		return web.template.render('template', base="layout", globals={
			'wunsch_select_wunsch': tpl.wunsch_select_wunsch,
			'wunsch_select_prio': tpl.wunsch_select_prio,
			'wunsch_prio': tpl.wunsch_prio,
			"monat_select": tpl.monat_select,
			'btn_cancel': tpl.btn_cancel,
			'btn_ok': tpl.btn_ok,
			'urls': urls,
			"session": session,
			"ctx": web.ctx,
			"strip_tags": strip_tags,
			"env": web.ctx.env,
			"config": config,
			"avatar": tpl.avatar
		})

	def person(self, pid, history):
		# get latest wishes
		if history == None:
			try:
				w = db.session.query(db.Wunsch).filter_by(pid=pid, latest=1)
			except:
				db.session.rollback()
		else:
			endd = history + datetime.timedelta(days=1)

			try:
				w = db.session.query(db.Wunsch).filter_by(pid=pid).filter(
					and_(db.Wunsch.created >= datetime.date(history.year, history.month, history.day),\
					db.Wunsch.created < datetime.date(endd.year, endd.month, endd.day))
				)
			except:
				db.session.rollback()
			
		#print u
		try:
			g = db.session.query(db.Group).order_by(db.Group.sort)
		except:
			db.session.rollback()
		
		# modified dates
		try:
			d = db.session.query(db.distinct(db.Wunsch.created)).filter_by(pid=pid)
		except:
			db.session.rollback()
		
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

class index(response):
	def GET(self):
		print "index class"
		
		# 1) get all due tasks
		due_date = datetime.datetime.utcnow() + datetime.timedelta(days=7)
		due = db.session.query(db.RotNote)\
		                .filter(db.RotNote.type == 2, db.RotNote.bis < due_date, db.RotNote.bis > 0)\
		                .order_by(db.RotNote.bis.asc())\
		                .order_by(db.RotNote.created.asc())
		
		dueids = []
		for d in due:
			dueids.append(d.id)
		print dueids
		
		# 2) get all other tasks
		tags = db.session.query(db.NoteTag).all()
		return self.render().index(web.ctx, tags, db.RotNoteType, due)
	
class erfahrung(response):
	def GET(self, path):
		id = None
		if path:
			id = path[1:]
		else:
			return "Missing pid"
		
		return self.render().erfahrung(id)

class rotnote(response):
	def GET(self, path):
		id = None
		if path:
			id = path[1:]
		else:
			web.header('Content-Type', 'application/json; charset=utf-8', unique=True)
			return '{"success": false, "error": "parameter id missing!"}'
		
		try:
			r = db.session.query(db.RotNote).filter_by(id=id)[0]
		except:
			db.session.rollback()
			web.header('Content-Type', 'application/json; charset=utf-8', unique=True)
			return '{"success": false, "error": "'+str(sys.exc_info()[0])+'"}'
		
		d = None
		if r.bis:
			d = r.bis.strftime("%d.%m.%Y")
		
		tags = []
		for t in r.tags:
			tags.append(t.name)
		
		response = {
			"id": r.id,
			"comment": r.comment,
			"bis": d,
			"done": r.done,
			"type": r.type,
			"tags": tags
		}
		web.header('Content-Type', 'application/json; charset=utf-8', unique=True)
		return '{"success": true, "data": '+json.dumps(response)+'}'
		
		
	def POST(self, path):
		id = None
		if path:
			id = int(path[1:])
		#print path, id
		p = web.input(action=None)
		tags = []
		# no tags on delete action
		try:
			if p.tags:
				tags = p.tags.split(",")
			print "tags " + str(tags)
		except: 
			pass
		
		# if we have an id, then we need to update or delete
		if id and p.action == "delete":
			print "Delete"
			try:
				r = db.session.query(db.RotNote).filter_by(id=id)[0]
				# remove existing tags
				for t in r.tags:
					r.tags.remove(t)
				#db.session.commit()
				
				db.session.delete(r)
				#db.session.commit()
				
				# FIXME: remove tags
			except:
				db.session.rollback()
				web.header('Content-Type', 'application/json; charset=utf-8', unique=True)
				return '{"success": false, "error": "'+str(sys.exc_info()[0])+'"}'
			
			web.header('Content-Type', 'application/json; charset=utf-8', unique=True)
			return '{"success": true, "id": '+str(id)+'}' 
		
		if id and p.action == "update":
			print "Update"
			# TODO: update tags
			try:
				r = db.session.query(db.RotNote).filter_by(id=id)[0]
				d = None
				if p.due:
					d = datetime.datetime.fromtimestamp(int(p.due))
					r.bis=d
				else:
					r.bis="0000-00-00"
				r.pid=p.pid
				r.comment=p.comment
				r.type=p.type
				#db.session.commit()
				
				"""
>>> t = r.tags[0]
>>> t
<rot_notetag(id='1')>
>>> r.tags.remove(t)
>>> db.session.commit()

>>> t = db.session.query(db.NoteTag).filter_by(name="USB")[0]
>>> t
<rot_notetag(id='1')>
>>> r.tags.append(t)
>>> r.tags
[<rot_notetag(id='1')>]
>>> db.session.commit()
				"""
				
				# remove existing tags
				db.session.begin()
				for t in r.tags:
					r.tags.remove(t)
				db.session.commit()
				
				# add new tags to note
				for t in tags:
					obj = db.session.query(db.NoteTag).filter_by(name=t)
					if obj.count() != 0: # existing
						obj = obj[0]
					else: # new
						obj = db.NoteTag(name=t)
						db.session.add(obj)
					
					r.tags.append(obj)
				#db.session.commit()
				
				print "pid     " + str(r.pid)
				print "comment " + str(r.comment)
				print "type    " + str(r.type)
				print "bis     " + str(r.bis)
				print "tags    " + str(tags)
				
			except:
				db.session.rollback()
				web.header('Content-Type', 'application/json; charset=utf-8', unique=True)
				return '{"success": false, "error": "'+str(sys.exc_info()[0])+'"}'
			web.header('Content-Type', 'application/json; charset=utf-8', unique=True) 
			return '{"success": true, "id": '+str(id)+'}'
				
		# insert acation
		try:
			print "Insert"
			d = None
			if p.due:
				d = datetime.datetime.fromtimestamp(int(p.due))
				n = db.RotNote(pid=p.pid, comment=p.comment, type=p.type, bis=d)
			else:
				n = db.RotNote(pid=p.pid, comment=p.comment, type=p.type, bis="0000-00-00")
			db.session.add(n)
			db.session.flush()
			print n
			
			# add new tags to note
			for t in tags:
				obj = db.session.query(db.NoteTag).filter_by(name=t)
				if obj.count() != 0: # existing
					obj = obj[0]
				else: # new
					obj = db.NoteTag(name=t)
					db.session.add(obj)
				
				n.tags.append(obj)
				
			
			#db.session.commit()
		except:
			web.header('Content-Type', 'application/json; charset=utf-8', unique=True)
			return '{"success": false, "error": "'+str(sys.exc_info()[0])+'"}'
		
		#print p
		web.header('Content-Type', 'application/json; charset=utf-8', unique=True) 
		return '{"success": true, "id": '+str(n.id)+'}'

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
		
		no_image = True
		path = ""
		try:
			tnpath = "static/thumbnails/"+pid+"_thumbnail.jpg"
			if not os.path.exists(tnpath):
				no_image = True
				r = db.session.query(db.Person).filter_by(pid=pid)[0]
				if r.foto_thumbnail != None:
					fp = open(tnpath, "w")
					fp.write(r.foto_thumbnail)
					fp.close()
					no_image = False
				else:
 					no_image = True
 			else:
				no_image = False
 			
 			if no_image == False:
				#web.header("Content-type", "image/jpeg")
				#fp = open(tnpath, "r")
				#img = fp.read()
				#fp.close()
			
				path = "../static/thumbnails/" + pid + "_thumbnail.jpg"
				if config.base_uri:
					path = config.base_uri + "static/thumbnails/" + pid + "_thumbnail.jpg"
		
		except:
			db.session.rollback()
			no_image = True
		
		# display std avatar
		#fp = open('static/avatar.svg', 'r')
		#buffer = fp.read()
		#fp.close()
		
		# send headers
		#web.header("Content-length", len(buffer))
		#web.header("Content-type", "image/svg+xml")
		if path == "":
			path = '../static/avatar.svg'
			if config.base_uri:
				path = config.base_uri+'static/avatar.svg'
		print path
		raise web.seeother(path)
	
	def POST(self, path):
		#print "Path: ", path
		pid = None
		if path:
			pid = path[1:]
		
		try:
			personal = db.session.query(db.Personal).filter_by(pid=pid)[0]
		except:
			db.session.rollback()
			# FIXME: handle DB Error
			#print personal
	
		if len(personal.rot_pers) == 0:
			p = db.Person()
			p.personal = personal
		else:
			p = personal.rot_pers[0]
	
		f = web.input(file={})
	
		p.foto = f["file"].value
	
		# write temp file
		path = "tmp/%s.jpg" % pid
		path_cropped = "tmp/%s_cropped.jpg" % pid
		path_thumbnail = "tmp/%s_thumbnail.jpg" % pid
		fd = open(path,'w')
		fd.write(f["file"].value) # python will convert \n to os.linesep
		fd.close()
	
		# crop and resize image
		import img
		img.portrait(path, width=300, out=path_cropped , thumbnail=path_thumbnail)
		
		print "reading %s" % path_cropped
		fd = open(path_cropped, 'r')
		p.foto_cropped = fd.read()
		fd.close()
		
	
		print "reading %s" % path_thumbnail
		fd = open(path_thumbnail, 'r')
		p.foto_thumbnail = fd.read()
		fd.close()
		
		# remove all temporary files
		"""
		os.remove(path)
		os.remove(path_cropped)
		"""
		try:
			os.remove("static/thumbnails/" + pid + "_thumbnail.jpg")
		except:
			pass
		print "copy file from %s to %s" % (
			path_thumbnail, "static/thumbnails/" + pid + "_thumbnail.jpg"
		)
		os.rename(path_thumbnail, "static/thumbnails/" + pid + "_thumbnail.jpg")
		#for e in f["file"]:
		#	print e
		
		# FIXME: handle errors
		#db.session.commit()
		#except Exception as e:
		#	exc_type, exc_obj, exc_tb = sys.exc_info()
		#	fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		#	print(exc_type, fname, exc_tb.tb_lineno)
		#
		#	db.session.rollback()
		
		self.header(content_type="application/json")
		return """
{"files": [
  {
    "name": """ + '"' + f["file"].filename + '"' + """,
    "size": """ + str(len(f["file"].value)) + """,
    "url": """ + "'http://localhost/upload/"+ str(p.id) + "'" + """,
    "thumbnailUrl": """ + "'http://localhost/upload/"+ str(p.id) + "'" + """,
    "deleteUrl": """ + "'http://localhost/upload/"+ str(p.id) + "'" + """,
    "deleteType": "POST"
  }
  ]
}
"""

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
		
		try:
			for p in db.session.query(db.Personal).\
				order_by(asc(db.Personal.name)).\
				with_entities(db.Personal.pid, db.Personal.name, db.Personal.vorname, db.Personal.kuerzel).\
				filter_by(aktiv=1, pidp=''):
				ret += json.dumps({"pid": p[0], "name": p[1], "vorname": p[2], "kuerzel": p[3]}, encoding=db.Personal.encoding) + ",\n"
				#ret += str(p.as_json()) + ",\n"
		except:
			db.session.rollback()
			# FIXME: handle DB Error
			
		return ret[:-2] + "]"

class typeahead(response):
	def GET(self):
		
		ret = 'var names = { "options": [';
		self.header(content_type="application/json")
		
		try:
			for p in db.session.query(db.Personal).\
				order_by(asc(db.Personal.name)).\
				with_entities(db.Personal.pid, db.Personal.name, db.Personal.vorname, db.Personal.kuerzel).\
				filter_by(aktiv=1, pidp=''):
				#ret += json.dumps({"pid": p[0], "name": p[1], "vorname": p[2], "kuerzel": p[3], "str": str(p[1]) + " " + str(p[2]) + " (" + str(p[3]) + ")"}, encoding=db.Personal.encoding) + ",\n"
				if not p[1]: p[1] = ""
				if not p[2]: p[2] = ""
				k = ""
				try:
					if not p[3]: 
						p[3] = ""
						k = ""
					else:
						k = p[3]
				except:
					pass
				ret += json.dumps({"pid": p[0], \
					"name": p[1], \
					"vorname": p[2], \
					"kuerzel": p[3], \
					"str": p[1] + " " + p[2] + \
					" (" + k + ")"}, encoding=db.Personal.encoding) + ",\n"
				#ret += str(p.as_json()) + ",\n"
		except:
			db.session.rollback()
			# FIXME: handle DB Error
			
		return ret[:-2] + "]}"

class personal(response):
	def GET(self, path=None):
		
		pid = None
		
		if path:
			#print "Path: " + path
			pid = path[1:]
			session["selected_pid"] = pid
		else:
			return self.render().personal(db.Personal(), {}, db.RotNoteType, {}, time.strftime("%Y%m%d"))
		
		# person und wuensch
		try:
			person = db.session.query(db.Personal).filter_by(pid=pid)[0]
		except:
			db.session.rollback()
			# FIXME: handle DB Error
			#print personal

		#person.person_add = db.session.query(db.Personal).filter_by(pidp=pid)
		try:
			wunsch = db.session.query(db.Wunsch)\
				.filter_by(pid=pid, latest=1)\
				.order_by(db.Wunsch.prio.asc())
		except:
			db.session.rollback()
			# FIXME: handle DB Error
		
		# get rotnote
		try:
			notes = db.session.query(db.RotNote)\
				.filter_by(pid=pid)\
				.order_by(db.RotNote.created.desc())
		except:
			db.session.rollback()
			# FIXME: handle DB Error
		
		# get all tags
		try:
			tags = db.session.query(db.NoteTag)\
				.order_by(db.NoteTag.name.desc())
		except:
			db.session.rollback()
			# FIXME: handle DB Error
		
		# alternative personen und vertraege
		"""
		vertraege = []
		person_parent = db.session.query(db.Personal).filter_by(pidp=pid)
		vert = db.session.query(db.Rotblock).filter_by(pid=pid)
		for v in vert:
			vertraege.apppend(v)
		
		for p in person_parent:
			vert = db.session.query(db.Rotblock).filter_by(pid=p.pid)
			for v in vert:
				vertraege.apppend(v)
		"""
		return self.render().personal(person, wunsch, db.RotNoteType, notes, time.strftime("%Y%m%d"), tags)
		#return "Hello World"

class wunsch(response):
	def GET(self, path):
		
		pid = None
		if path:
			#print "Path: " + path
			pid = path[1:]
			session["selected_pid"] = pid
		else:
			return "No pid"
		
		history = None
		try:
			h = web.input(name="history").history
			h2 = time.strptime(h, "%d.%m.%Y")
			history = datetime.datetime(h2.tm_year, h2.tm_mon, h2.tm_mday)
		except: pass
		#print history
		
		# get user info
		try:
			u = db.session.query(db.Personal).filter_by(pid=pid)[0]
		except:
			db.session.rollback()
		
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
		
		(g, wunsch, dates) = self.person(pid, history)
		
		#return render.wunsch(g, u, wunsch, dates, history)
		return self.render().wunsch(g, u, wunsch, dates, history)
		#return "Hello World"
	
	def POST(self, pid):
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
		try:
			lw = db.session.query(db.Wunsch).filter_by(pid=pid, latest=1)
		except:
			db.session.rollback()
			# FIXME: handle DB Error

		for l in lw:
			l.latest = 0
		#db.session.commit()
		
		# get rid of records with the current date
		dt = datetime.datetime.now()
		try:
			lw = db.session.query(db.Wunsch).filter(db.Wunsch.created >= datetime.date(dt.year, dt.month, dt.day))
		except:
			db.session.rollback()
			# FIXME: handle DB Error
		for l in lw:
			db.session.delete(l)
		#db.session.commit()
		
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
		#db.session.commit()
