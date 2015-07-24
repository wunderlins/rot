#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web, config, json, db
import datetime
import time
from sqlalchemy import *
import tpl
import re
import base64
import sys
import os
import usbauth
import hashlib
import sqlite3

urls = (
	'/', 'webctx.index',
	'/personal(.*)', 'webctx.personal',
	'/personal_data', 'webctx.personal_data',
	'/test', 'webctx.test', # test methods, remove these in production
	'/wunsch(.*)', 'webctx.wunsch', # test methods, remove these in production
	'/wunsch_save(.*)', 'webctx.wunsch',
	'/typeahead', 'webctx.typeahead',
	'/image(.*)', 'webctx.image',
	'/rotnote(.*)', 'webctx.rotnote',
	'/erfahrung(.*)', 'webctx.erfahrung',
	'/login', 'webctx.login',
	'/plan', 'webctx.plan',
	'/get_plan', 'webctx.get_plan',
	'/get_meta', 'webctx.get_meta',
	'/get_month', 'webctx.get_month',
	'/get_emp', 'webctx.get_emp',
	'/update_rot', 'webctx.update_rot'
)

from HTMLParser import HTMLParser

"""
try:
	session
except:
	web.debug("==> Resetting session!")
	session = None

"""

web.debug("==> Resetting session!")
session = None

"""
# FIXME: add a separate uid, next to pid
#        pid: planoaa person id
#        eid: ad employee id
session_default = {
	"selected_pid": 0,
	"eid": None,
	"pid": None,
	"user": None,
	"isadmin": False
}
"""

"""
def set_session(n, v):
	global session
	if session == None:
		session = {}
	session[n] = v

def get_session():
	global session
	return session
"""

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
	
	"""
	#session = get_session()
	session = get_session()
	if session == None:
		for e in session_default:
			set_session(e, session_default[e])
	"""
	print session
	print "session: "
	for e in session:
		print "%s, %s" % (e, session[e])
	
	auth = web.ctx.env.get('HTTP_AUTHORIZATION')
	if auth is not None and session.user == None:
		session.user = None
		auth = re.sub('^Basic ', '', auth)
		username, password = base64.decodestring(auth).split(':')
		#print username,password
		if (username, password) in allowed:
			#print "allowd"
			session.user = username
			session.pid = 0
			session.selected_pid = 0
			return
	
	if session["user"] == None:
		web.header('WWW-Authenticate','Basic realm="Auth example"')
		web.ctx.status = '401 Unauthorized'
		return

class response:
	no_auth = False
	__authenticated = False
	
	def __init__(self):
		web.debug("> class " + self.__class__.__name__)
		"""
		Every response object will, when instatiated, do a basic authentication.
		
		This is globally applied for now, that means, there is no way to serve pages to anonymous users.
		
		Not sure if this is a sane way.
		
		"""
		"""
		session = get_session()
		if session == None:
			web.debug("==> session init in response.__init__")
			for e in session_default:
				set_session(e, session_default[e])
		"""
	def header(self, content_type="text/html"):
		web.header('Content-Type', content_type+'; charset=utf-8', unique=True) 
		web.header('Cache-Control','no-cache, no-store, must-revalidate')
		web.header('Pragma','no-cache')
		web.header('Expires','0')
	
	def render(self, base="layout"):
		global urls
		#session = get_session()
		print session
		return web.template.render('template', base=base, globals={
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
			"avatar": tpl.avatar,
			"type": type, 
			"input": web.input()
		})
		
	def auth_check(self):
		""" check if user is authenticated """
		
		"""
		try:
			web_session.pid
		except:
			web.debug("creating session")
			for e in session_default:
				web_session[e] = session_default[e]
		"""
		
		#web_session = get_session()
		#session = get_session()
		
		# check if we have a valid session
		#print session
		if session != None and session.eid >= 0:
			web.debug("==> Autenticated")
			self.__authenticated = True
			return True
		
		# authentication for this request not required
		if self.no_auth == True:
			return True
			
		# check if the user has submitted credentials
		web.debug("==> NOT Autenticated")
		web.debug(web.config.get('_session'))
		return None
	
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

	def json(self, obj):
		web.header('Content-Type', 'application/json; charset=utf-8', unique=True)
		#web.config.debug = False
		if web.config.debug:
			return json.dumps(obj, encoding="utf-8", indent=2)
		else:
			return json.dumps(obj, encoding="utf-8")

class login(response):
	no_auth = True
	
	def GET(self):
		#global web_session
	
		user_data = web.input(logout=False)
		web.debug(user_data.logout)
		if (user_data.logout == "true"):
			session.kill()
			raise web.seeother(config.base_uri + "/")
	
	""" authenticate user """
	def POST(self):
		#global web_session
		
		# read posted json data
		data = web.data()
		credentials = json.loads(data)
		
		username = credentials["username"]
		password = credentials["password"]
		
		# check credentials against database
		pwhash = hashlib.md5(password).hexdigest()
		web.debug(pwhash)
		authdb = sqlite3.connect('etc/user.db')
		cur = authdb.cursor()
		sql = 'SELECT id FROM user WHERE username=? AND password=?'
		web.debug(sql)
		check = cur.execute(sql, (username, pwhash))
		web.debug(str(check) + " " + str(cur.rowcount))
		
		a = [username in config.adminuser][0]
		if check:
			row = cur.fetchone()
			if row:
				authdb.close()
				web.debug("username " + str(row))
				#web_session = session_default
				session.pid = row[0]
				#set_session("selected_pid", row[0])
				session.eid = 0
				session.user = username
				session.isadmin = True
			
				# if we found one, exit
				return '{"success": true}'
		
		authdb.close()
		
		# if not found check against ldap
		usbauth.init(
			authdn = "CN=MUANA,OU=GenericMove,OU=Users,OU=USB,DC=ms,DC=uhbs,DC=ch",
			authpw = "anaana",
			baseDN = "ou=USB,dc=ms,dc=uhbs,dc=ch",
			host = "ms.uhbs.ch",
		)
		
		emp = usbauth.check(username, password)
		#global session
		web.debug(session)
		if (emp and emp["lockoutTime"] == None):
			#web_session = session_default
			session.pid = 0
			session.eid = emp["employeeNumber"]
			session.user = username
			session.email = emp["email"]
			session.isadmin = a
			
			# now that we have a user, find the pid for this uid
			ret = db.session.query(db.Personal).\
			         filter_by(personalid=emp["employeeNumber"]).all()
			#web.debug("pid: " + str(ret[0].pid))
			
			try:
				session.pid = ret[0].pid
			except:
				pass # FIXME do we have to catch unknown pids on login or just ignore ?
			
			web.debug("==> succesfully logged in")
			web.debug(session)
			
			return '{"success": true}'
		
		return '{"success": false}'

class get_emp(response): 
	"""
	rbid, pid, rvon, rbis, kuerzel, anrede, name, vorname, email, combi
	"""
	def GET(self):
		von = web.input(von=None)
		bis = web.input(bis=None)

		sql = db.text("""SELECT rb.rbid, p.pid, rb.rvon, rb.rbis, p.kuerzel, p.anrede, p.name, p.vorname, p.email, p.combi
						FROM rotblock rb LEFT JOIN personal p ON (rb.pid = p.pid)
						WHERE (rvon <= '"""+str(von.von)+"""' and rbis >= '"""+str(von.von)+"""' OR 
						       rvon <= '"""+str(bis.bis)+"""' and rbis >= '"""+str(bis.bis)+"""')
						 AND p.ptid = 4
						 
						ORDER BY p.kuerzel """)

		res = db.engine.execute(sql)
		
		ret = {"count": 0, "root" : []}
		#ret["root"].append([0, "", 0, 0, 0, "", 0, 0, "Leer", ""]) # empty record
		
		for r in res:
			row = [
			#	[0, "", 0, 0, 0, "", 0, 0, "", ""] # empty record
			]
			
			for e in r:
				row.append(e)
			ret["root"].append(row)
			ret["count"] += 1
		
		web.header('Content-Type', 'application/json; charset=utf-8', unique=True)
		return self.json(ret)
		
		
class get_month(response):
	def GET(self):
		ym  = web.input(ym=None)
		#von = web.input(von=None)
		#bis = web.input(bis=None)
		
		
		if ym == None:
			web.header('Content-Type', 'application/json; charset=utf-8', unique=True)
			return '{"root": [], "count": 0 }'
		
		'''
			sql = db.text("""SELECT r.rid, p.kuerzel, p.ptid,
							 r.pid, r.bgrad, r.bemerkung2 as comment,
							 c.fg, c.bg, p.name, p.vorname

				FROM rotation r LEFT JOIN personal p on (r.pid = p.pid)
								        LEFT JOIN color c on (r.cid = c.cid)

				WHERE 1=1
					AND r.jm = '"""+str(ym.ym)+"""'
					AND r.pid IN (SELECT rb.pid as id
						FROM rotblock rb LEFT JOIN personal p ON (rb.pid = p.pid)
						WHERE (rvon <= '"""+str(von.von)+"""' and rbis >= '"""+str(von.von)+"""' OR 
						       rvon <= '"""+str(bis.bis)+"""' and rbis >= '"""+str(bis.bis)+"""')
						      AND p.ptid = 4)

				ORDER BY p.kuerzel ASC""")
		'''
		sql = db.text("""SELECT r.rid, p.kuerzel, p.ptid,
						 r.pid, r.bgrad, r.bemerkung2 as comment,
						 c.fg, c.bg, p.name, p.vorname, r.rbid, r.rtyp

			FROM rotation r LEFT JOIN personal p on (r.pid = p.pid)
								      LEFT JOIN color c on (r.cid = c.cid)

			WHERE 1=1
				AND r.jm = '"""+str(ym.ym)+"""'
				AND r.pid IN (SELECT rb.pid as id
					FROM rotblock rb LEFT JOIN personal p ON (rb.pid = p.pid)
					WHERE rvon <= '"""+str(ym.ym)+"""' and rbis >= '"""+str(ym.ym)+"""' and p.ptid = 4)

			ORDER BY p.kuerzel ASC""")

		res = db.engine.execute(sql)
		
		ret = {"count": 0, "root" : []}
		ret["root"].append([0, " ", 0, 0, 0, "", 0, 0, "Leer", " ", 0, 0])
		
		for r in res:
			row = []
			for e in r:
				row.append(e)
			ret["root"].append(row)
			ret["count"] += 1
		
		
		web.header('Content-Type', 'application/json; charset=utf-8', unique=True)
		return self.json(ret)

class get_meta(response):
	def GET(self):
		# get user input
		try:
			von = web.input(von=None).von
			bis = web.input(von=None).bis
		except:
			return self.json({
				"success": False,
				"root": {},
				"count": 0,
				"error": "failed to parse input."
			})
		
		return self.json(data.plan_meta(von, bis))
	

class data:
	
	# von bis are dates, format yyyymm (4digit year, 2 digit month)
	@staticmethod
	def plan_meta(von, bis): 
		months = 0
		cellwidth = 80
		padding = 7
		
		# validate user input
		try:
			date_sel = {
				"von": {
					"m": von[4:],
					"y": von[0:4] 
				},
				"bis": {
					"m": bis[4:],
					"y": bis[0:4] 
				}
			}

		except:
			return {
				"success": False,
				"root": None,
				"count": 0,
				"error": "failed to parse input."
			}
			
		# metadata
		ret = {"count": 0, "root" : None, "metaData": None}
		ret["metaData"] = {
			#"root": "root",
			"von": von,
			"bis": bis,
			"date_sel": date_sel,
			"months": 0,
			"error": None,
			"fields" : [
				{"type": 'int', "mapping": 0, "name": 'id'},
				{"type": 'int', "mapping": 1, "name": 'rid'},
				{"type": 'string', "mapping": 2, "name": "group_sort"},
				{"type": 'string', "mapping": 3, "name": "rot_group"},
				{"type": 'string', "mapping": 4, "name": 'name'},
				{"type": 'string', "mapping": 5, "name": 'description'},
				{"type": 'string', "mapping": 6, "name": 'srt'},
			],
			"columns": [
				{
					"xtype": 'gridcolumn', 
					"hidden": True,
					"text": 'Id', 
					"dataIndex": 'id', 
					"width": 40, 
					"locked": True
				},{
					"xtype": 'gridcolumn', 
					"text": "group_sort", 
					"dataIndex": "group_sort", 
					"width": 60,
					"draggable": False,
					"resizable": False,
					"hideable": False,
					"menuDisabled": True,
					"sortable": False,
					"hidden": True,
					"locked": True
				},{
					"xtype": 'gridcolumn', 
					"text": "rot_group", 
					"dataIndex": "rot_group", 
					"hidden": True,
					"locked": False
				},{
					"xtype": 'gridcolumn', 
					"text": 'Name', 
					"dataIndex": 'name', 
					"width": 180,
					"draggable": False,
					"resizable": False,
					"hideable": False,
					"menuDisabled": True,
					"sortable": False,
					"locked": True
				},{
					"xtype": 'gridcolumn', 
					"text": 'Description', 
					"dataIndex": 'description', 
					"width": 60, 
					"width": 150,
					"hidden": True
				},{
					"xtype": 'gridcolumn', 
					"text": 'Sort', 
					"dataIndex": 'srt', 
					"width": 60, 
					"width": 150,
					"hidden": True
				},
				{"text": str(date_sel["von"]["y"]), "columns": [], "menuDisabled": True}
			]
		}
		
		# pointer to last year
		currenty = ret["metaData"]["columns"][len(ret["metaData"]["columns"])-1]
		
		# count number of months
		tmp = date_sel["von"]
		tmp["y"] = int(tmp["y"])
		tmp["m"] = int(tmp["m"])
		web.debug("counting months %d %d" % (tmp["m"], tmp["y"]))
		n = ""
		amonth = []
		while tmp["m"] != int(date_sel["bis"]["m"]) or tmp["y"] != int(date_sel["bis"]["y"]):
			#web.debug(str(months))
			n = "" + str(tmp["y"]);
			if tmp["m"] < 10:
				n = n + "0" + str(tmp["m"])
			else: 
				n = n + str(tmp["m"]);
			
			amonth.append(n)
			
			currenty["columns"].append({
				"xtype": 'gridcolumn', 
				"text": str(tmp["m"]), 
				"dataIndex": n, 
				"width": cellwidth,
				"draggable": False,
				"resizable": False,
				"hideable": False,
				"menuDisabled": True,
				"sortable": False,
				"renderer": "rot.grid.cell_renderer",
				#"editor": {
				#	"xtype": "combobox",
				#	"store": "monthempStore",
				#	"displayField": "kuerzel",
				#	"valueField": "pid",
				#	"selectOnFocus": True,
				#	"selectOnTab": True,
				#	"autoSelect": True,
				#	"caseSensitive": False,
				#	"maxLength": 3,
				#	"queryMode": "local",
				#	"typeAhead": True,
				#	"allowBlank": True,
				#	"validateBlank": True,
				#	"autoLoadOnValue": True,
				#	"forceSelection": True
				#},
			})
			
			ret["metaData"]["fields"].append({
				"type": 'string', 
				"mapping": months + padding, 
				"name": n
			})
			
			tmp["m"] += 1
			if tmp["m"] == 13:
				tmp["y"] += 1
				tmp["m"] = 1
				
				col = {"text": str(tmp["y"]), "columns": [], "menuDisabled": True}
				ret["metaData"]["columns"].append(col)
				currenty = ret["metaData"]["columns"][len(ret["metaData"]["columns"])-1]
			
			months += 1
		#web.debug(str(months))
		# add last month
		months += 1
		n = "" + str(tmp["y"]);
		if tmp["m"] < 10:
			n = n + "0" + str(tmp["m"])
		else: 
			n = n + str(tmp["m"]);
		
		amonth.append(n)
		
		currenty["columns"].append({
			"xtype": 'gridcolumn', 
			"text": str(tmp["m"]), 
			"dataIndex": n, 
			"width": cellwidth,
			"draggable": False,
			"resizable": False,
			"hideable": False,
			"menuDisabled": True,
			"sortable": False,
			#"editor": {
			#	"xtype": "combobox",
			#	"store": "monthempStore",
			#	"displayField": "kuerzel",
			#	"valueField": "pid",
			#	"selectOnFocus": True,
			#	"selectOnTab": False,
			#	"autoSelect": True,
			#	"caseSensitive": False,
			#	"maxLength": 3,
			#	"queryMode": "local",
			#	"typeAhead": True,
			#	"allowBlank": True,
			#	"validateBlank": True,
			#	"autoLoadOnValue": True
			#},
			"renderer": "rot.grid.cell_renderer"
		})
		
		ret["metaData"]["fields"].append({
			"type": 'string', 
			"mapping": months + padding, 
			"name": n
		})
		
		ret["metaData"]["months"] = months
		ret["metaData"]["padding"] = padding
		ret["metaData"]["amonth"] = amonth
				
		return ret

class update_rot(response):
	def GET(self):
		try:
			id = int(web.input(von=None).id)
			pid = int(web.input(von=None).pid)
			rid = int(web.input(von=None).rid)
			rbid = int(web.input(von=None).rbid)
			y = int(web.input(von=None).y)
			m = int(web.input(von=None).m)
			kuerzel = web.input(von=None).kuerzel
			ym = web.input(von=None).ym
			old = web.input(von=None).old
			
			rec = {
				"id": id,
				"pid": pid,
				"rid": rid,
				"rbid": rbid,
				"m": m,
				"y": y,
				"kuerzel": kuerzel,
				"ym": ym,
				"old": old
			}
		
		except:
			return self.json({
				"success": False,
				"root": {},
				"count": 0,
				"error": "failed to parse input."
			})
		
		#try:
		#web.debug(rec)
		
		if rec["pid"] == 0: # clear existing assignement
			# find pid	
			sql = """SELECT p.pid
				FROM personal p LEFT JOIN rotblock r ON (p.pid = r.pid)
				WHERE p.kuerzel = '""" + rec["old"] + """'
					AND r.rvon <= '""" + rec["ym"] + """' AND r.rbis >= '""" + rec["ym"] + """' """
			res = db.engine.execute(db.text(sql))
			
			#web.debug(res)
			pid = None
			for r in res:
				web.debug(r)
				pid = r[0]
				break
			
			rot = db.session.query(db.Rotation)\
					            .filter(db.Rotation.jm == rec["ym"], \
					                    db.Rotation.pid == pid)
			
			#web.debug(rot[0])
			rot[0].rtyp = 0
			db.session.flush()
			#web.debug(rot[0].rtyp)
			
		else: # set new assignement
			# update rotation with rot id
			rot = db.session.query(db.Rotation)\
					            .filter(db.Rotation.jm == rec["ym"], \
					                    db.Rotation.pid == rec["pid"], \
					                    db.Rotation.rbid == rec["rbid"])
	
			rot[0].rtyp = rec["rid"]
			db.session.flush()
			web.debug(rot[0].rtyp)
		
		"""
		except:
			return self.json({
				"success": False,
				"root": {},
				"count": 0,
				"error": "failed to update database."
			})
		"""
		return self.json({
			"success": True,
			"root": rec,
			"count": 1,
			"error": ""
		})
		
class get_plan(response):
	def GET(self):
		
		# get user input
		try:
			von = web.input(von=None).von
			bis = web.input(von=None).bis
		except:
			return self.json({
				"success": False,
				"root": {},
				"count": 0,
				"error": "failed to parse input."
			})
			
		"""
		months = 0
		cellwidth = 50
		
		date_sel = {
			"von": {
				"m": von[4:],
				"y": von[0:4] 
			},
			"bis": {
				"m": bis[4:],
				"y": bis[0:4] 
			}
		}

		# metadata
		ret = {"count": 0, "root" : [], "metaData": None}
		ret["metaData"] = {
			#"root": "root",
			"von": von,
			"bis": bis,
			"date_sel": date_sel,
			"months": 0,
			"error": None,
			"fields" : [
				{"type": 'int', "mapping": 0, "name": 'id'},
				{"type": 'string', "mapping": 1, "name": "rot_group"},
				{"type": 'string', "mapping": 2, "name": 'name'},
			],
			"columns": [
				{
					"xtype": 'gridcolumn', 
					"hidden": True,
					"text": 'Id', 
					"dataIndex": 'id', 
					"width": 40, 
					"locked": True
				},{
					"xtype": 'gridcolumn', 
					"text": "rot_group", 
					"dataIndex": "rot_group", 
					"width": 60,
					"draggable": False,
					"resizable": False,
					"hideable": False,
					"menuDisabled": True,
					"sortable": False,
					"hidden": True,
					"locked": True
				},{
					"xtype": 'gridcolumn', 
					"text": 'Name', 
					"dataIndex": 'name', 
					"width": 60, 
					"width": 150,
					"locked": True
				}, {"text": str(date_sel["von"]["y"]), "columns": [], "menuDisabled": True}
			]
		}
		
		# pointer to last year
		currenty = ret["metaData"]["columns"][len(ret["metaData"]["columns"])-1]
		
		# count number of months
		tmp = date_sel["von"]
		tmp["y"] = int(tmp["y"])
		tmp["m"] = int(tmp["m"])
		web.debug("counting months %d %d" % (tmp["m"], tmp["y"]))
		n = ""
		while tmp["m"] != int(date_sel["bis"]["m"]) or tmp["y"] != int(date_sel["bis"]["y"]):
			#web.debug(str(months))
			n = "" + str(tmp["y"]);
			if tmp["m"] < 10:
				n = n + "0" + str(tmp["m"])
			else: 
				n = n + str(tmp["m"]);
			
			currenty["columns"].append({
				"xtype": 'gridcolumn', 
				"text": str(tmp["m"]), 
				"dataIndex": n, 
				"width": cellwidth,
				"draggable": False,
				"resizable": False,
				"hideable": False,
				"menuDisabled": True,
				"sortable": False
			})
			
			ret["metaData"]["fields"].append({
				"type": 'int', 
				"mapping": months+3, 
				"name": n
			})
			
			tmp["m"] += 1
			if tmp["m"] == 13:
				tmp["y"] += 1
				tmp["m"] = 1
				
				col = {"text": str(tmp["y"]), "columns": [], "menuDisabled": True}
				ret["metaData"]["columns"].append(col)
				currenty = ret["metaData"]["columns"][len(ret["metaData"]["columns"])-1]
			
			months += 1
		web.debug(str(months))
		# add last month
		months += 1
		n = "" + str(tmp["y"]);
		if tmp["m"] < 10:
			n = n + "0" + str(tmp["m"])
		else: 
			n = n + str(tmp["m"]);
		
		currenty["columns"].append({
			"xtype": 'gridcolumn', 
			"text": str(tmp["m"]), 
			"dataIndex": n, 
			"width": cellwidth,
			"draggable": False,
			"resizable": False,
			"hideable": False,
			"menuDisabled": True,
			"sortable": False
		})
		ret["metaData"]["fields"].append({
			"type": 'int', 
			"mapping": months+3, 
			"name": n
		})
		ret["metaData"]["months"] = months
		"""
		
		ret = data.plan_meta(von, bis)
		sql = db.text("""
			SELECT rr.id rrid, CONCAT("sort", LPAD(rg.sort, 3, '0')) as groupsort, rg.name groupname, rr.name rotname, 
			       rr.bemerkung, CONCAT(rg.sort, LPAD(rr.sort*100, 5, '0')) sort
			FROM rot_rot rr LEFT JOIN rot_group rg ON (rr.group_id = rg.id)
			ORDER BY rg.sort, rr.sort""")
		
		res = db.engine.execute(sql)
		
		rot_lookup = {}
		
		ret["root"] = []
		ret["metaData"]["maxid"] = 0;
		rid = 0;
		for r in res:
			
			try:
				rot_lookup[r[0]].append(rid)
			except:
				rot_lookup[r[0]] = [rid]
			
			#web.debug(r)
			row = [rid]
			rid += 1
			if r[0] > ret["metaData"]["maxid"]:
				ret["metaData"]["maxid"] = r[0]
			# add metadata
			for e in r:
				row.append(e)
				
			# add empty cell values
			c = 0
			while c < ret["metaData"]["months"]:
				row.append("")
				c += 1
			
			ret["root"].append(row)
			ret["count"] += 1
		
		# build a lookup table for months
		cell_lookup = {}
		ix = 0
		for e in ret["metaData"]["amonth"]:
			cell_lookup[int(e)] = (ix + ret["metaData"]["padding"])
			ix += 1
		#web.debug(cell_lookup)
		# create the relevant cell data according to the rotation table
		
		# fetch data from rotation
		sql = """SELECT r.rid, p.kuerzel, r.jm,
				   r.pid, r.bgrad, r.bemerkung2 as comment,
				   r.rtyp
									 

						FROM rotation r LEFT JOIN personal p on (r.pid = p.pid)
												    LEFT JOIN color c on (r.cid = c.cid)

						WHERE 1=1
							AND (r.jm >= '""" + ret["metaData"]["von"] + """' AND r.jm <= '""" + ret["metaData"]["bis"] + """')
				                AND p.ptid = 4
				                AND r.rtyp > 0

						ORDER BY r.rtyp, r.jm"""		
		
		res = db.engine.execute(db.text(sql))
		
		#web.debug(rot_lookup)
		
		# loop over all assignements, merge them with grid data
		for r in res:
			# r.rid, p.kuerzel, r.jm, r.pid, r.bgrad, r.bemerkung2 as comment, r.rtyp
			cell_ix = cell_lookup[int(r[2])]
			rot_ix = rot_lookup[r[6]] # the row index in the prefilled matrix
			
			# check if cell in rot is already fileld, if so, add a cloned empty cell
			done = False
			for i in rot_ix:
				if ret["root"][i][cell_ix] == "":
					ret["root"][i][cell_ix] = r[1]
					done = True
					break
			
			# if we could not fill an existing field, create a new row and add the 
			# cell. CAVE: make sure the sort value is correct
			if done != True:
				new_row = list(ret["root"][rot_ix[len(rot_ix)-1]]) # copy, not reference
				new_row[0] = len(ret["root"])
				#new_row[1] = ret["metaData"]["maxid"]
				#web.debug(new_row)
				new_sort = int(new_row[ret["metaData"]["padding"] - 1]) + 1
				new_row[ret["metaData"]["padding"] - 1] = unicode(new_sort)
				# now empty all data fields
				for i in range(ret["metaData"]["padding"], \
					             ret["metaData"]["padding"]+ret["metaData"]["months"]):
					new_row[i] = ""
			
				new_row[cell_ix] = r[1]
				ret["root"].append(new_row)
				rot_lookup[r[6]].append(len(ret["root"])-1)
		
		return self.json(ret)
		#return json.dumps(ret, encoding="utf8")
			
		'''
		return """{"root": [
			[0, "Rotation 1", "Herz"], 
			[1, "Rotation 2", "Herz"],
			[3, "Rotation 3", "Herz"],
			[4, "Rotation 4", "Herz"]
		]}"""
		'''
		#return '{"root": [{"id": 0, "name": "Rotation 1"}, {"id": 1, "name": "Rotation 2"}]}'
	
	
	
class plan:
	def GET(self):
		# open static index file, read it and return it
		#print os.path.dirname(os.path.realpath(__file__))
		fp = open('static/rot/index.html', 'r')
		content = fp.read()
		fp.close()
		
		# inject base tag after opening head tag
		base = '<base href="static/rot/" target="_blank">'
		content = content.replace("<head>", "<head>" + base);
		
		# sencha architect is unable to set the title tag properly, do it here! WTF
		reg = re.compile( '<title>[^<]+</title>')
		content = reg.sub("<title>Rotationsplan</title>", content)
		
		return content

class index(response):
	def GET(self):
		if not self.auth_check():
			return self.render(base=None).login()
		
		# check if the user is allowed to access this page, otherwise redirect
		if not session["isadmin"]:
			path = config.base_uri+'/personal/' + str(session["pid"])
			raise web.seeother(path)			
		
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
		
		"""
		remaining_comments = db.session.query(db.RotNote).join(db.rotnote2notetags)\
		                               .join(db.NoteTag)\
		                               .filter(~db.NoteTag.id.in_(dueids))
		
		db.session.query(db.RotNote).filter(db.RotNote.tags.any(~db.NoteTag.id.in_([1,2,3]))).all()
		"""
		
		return self.render().index(web.ctx, tags, db.RotNoteType, due)
	
class erfahrung(response):
	
	# TODO: should move this to the db module
	erftype = [
		"Anästhesie",
		"Intensiv",
		"Innere",
		"Chirurgie",
		"Anderes"
	]
	
	def GET(self, path):
		if not self.auth_check():
			return self.render(base=None).login()
		
		#session = get_session()
		
		pid = None
		if path:
			#print "Path: " + path
			pid = path[1:]
			session.selected_pid = pid
		else:
			pid = session.pid
		
		erf = db.session.query(db.Erfahrung).filter_by(pid=pid).all()
		#print erf
		"""
		id = None
		if path:
			id = path[1:]
		else:
			return "Missing pid"
		"""
		return self.render().erfahrung(pid, erf, self.erftype)

	def POST(self, path):
		if not self.auth_check():
			return self.render(base=None).login()
		
		pid = None
		if path:
			#print "Path: " + path
			pid = path[1:]
			session.selected_pid = pid
		else:
			pid = session.pid
		
		inp = json.loads(web.data())
		print inp
		
		
		# loop over "erfahrung"
		r = db.session.query(db.Erfahrung).filter_by(pid=pid).all()
		# remove existing tags
		for e in r:
			print e
			db.session.delete(e)
		db.session.flush()
		
		# import all "weiterbilduungen"
		for e in inp["erfahrung"]:
			d = None
			t = None
			if (e["dauer"]):
				d = int(e["dauer"])
			if (e["typ"]):
				t = int(e["typ"])
			r = db.Erfahrung(pid=int(pid), \
			                 von_mj=int(e["von"]), \
			                 monate=d, \
											 typ=t, \
			                 ort=e["ort"], \
			                 was=e["was"])
			db.session.add(r)
		db.session.flush()
		
		web.header('Content-Type', 'application/json; charset=utf-8', unique=True)
		return '{"success": true, "data": null}'
		
		path = config.base_uri+'/erfahrung/' + str(pid)
		#raise web.seeother(path)
		
		# ATLS, ACLS, PALS


class rotnote(response):
	def GET(self, path):
		if not self.auth_check():
			return self.render(base=None).login()
		
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
		if not self.auth_check():
			return self.render(base=None).login()
		
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
				db.session.flush()
				
				# FIXME: remove tags
			except:
				db.session.rollback()
				web.header('Content-Type', 'application/json; charset=utf-8', unique=True)
				return '{"success": false, "error": "'+str(sys.exc_info()[0])+'"}'
			
			web.header('Content-Type', 'application/json; charset=utf-8', unique=True)
			return '{"success": true, "id": '+str(id)+'}' 
		
		if id and p.action == "update":
			print "Update"
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
		if not self.auth_check():
			return self.render(base=None).login()
		
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
		if not self.auth_check():
			return self.render(base=None).login()
		
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
				path = config.base_uri+'/static/avatar.svg'
		print path
		raise web.seeother(path)
	
	def POST(self, path):
		if not self.auth_check():
			return self.render(base=None).login()
		
		#print "Path: ", path
		pid = None
		if path:
			pid = path[1:]
		
		try:
			personal = db.session.query(db.Personal).filter_by(pid=pid)[0]
		except:
			db.session.rollback()
	
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
		if not self.auth_check():
			return self.render(base=None).login()
		
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
		if not self.auth_check():
			return self.render(base=None).login()
		
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
		if not self.auth_check():
			return self.render(base=None).login()
		
		#session = get_session()
		
		pid = 0
		
		if path:
			#print "Path: " + path
			pid = path[1:]
			session.selected_pid = pid
		else:
			# return self.render().personal(db.Personal(), {}, db.RotNoteType, {}, time.strftime("%Y%m%d"))
			pid = session.pid
			web.debug(session)
		
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
		
		
		# erfahrung
		erfahrung = db.session.query(db.Erfahrung)\
			.order_by(db.Erfahrung.von_mj.desc())
		
		
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

		# normal user gets simple template
		if not session.isadmin:
			return self.render().personal_simple(person, wunsch, db.RotNoteType, notes, \
				                            time.strftime("%Y%m%d"), tags, erfahrung)

		return self.render().personal(person, wunsch, db.RotNoteType, notes, \
		                              time.strftime("%Y%m%d"), tags, erfahrung)
		#return "Hello World"

class wunsch(response):
	def GET(self, path):
		if not self.auth_check():
			return self.render(base=None).login()
		
		#session = get_session()
		pid = None
		if path:
			#print "Path: " + path
			pid = path[1:]
			session.selected_pid = pid
		else:
			pid = session.pid
		
		#print pid
		
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
		if not self.auth_check():
			return self.render(base=None).login()
		
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
		
		# delete all latest flags
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
		
		path = config.base_uri+'/wunsch/' + str(pid)
		raise web.seeother(path)

if config.web_debug:
	usbauth.usbauth.debug = True
