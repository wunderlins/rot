#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Start application server on port 8080

The first command line argument will set the port to be bound. Remeber, you 
need root privvileges to bind ports below 1024.

"""

import os, sys
#os.chdir(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib', 'web'))

import web, config, json, db
import datetime
import time
from sqlalchemy import *
import tpl
from webctx import *
import tempfile

session_default = {
	"selected_pid": 0,
	"pid": None,
	"user": None
}

def unloadhook():
	db.connection.close()
	
def loadhook():
	print datetime.datetime.now().strftime("%Y-%m-%d %H.%M.%S") + "\t" +\
	web.ctx.method + "\t" + \
	web.ctx.env.get('REQUEST_URI')

# allow to pass a custom port/ip into the application
class rot(web.application):
	def run(self, port=8080, ip='0.0.0.0', *middleware):
		func = self.wsgifunc(*middleware)
		return web.httpserver.runsimple(func, (ip, port))

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
			when = "D",
			interval = 1,
			backups = 1000
		)

def init_session():
	if web.config.get('_session') is None:
		web.config.session_parameters['cookie_name'] = 'rot'
		web.config.session_parameters['cookie_domain'] = None
		web.config.session_parameters['timeout'] = config.session_timeout,
		web.config.session_parameters['ignore_expiry'] = True
		web.config.session_parameters['ignore_change_ip'] = False
		web.config.session_parameters['secret_key'] = config.session_salt
		web.config.session_parameters['expired_message'] = 'Session expired'
		
		temp = tempfile.mkdtemp(dir=config.session_dir, prefix='session_')
		set_session(web.session.Session(
			app, 
			web.session.DiskStore(temp), 
			initializer = session_default
		))
		
	else:
		set_session(web.config._session)
		try:
			web.sess["pid"]
		except:
			set_session(session_default)


"""
def application(environ, start_response):

	# redirect webserver logs to file
	#weblog = open(config.web_logfile, "ab")
	#sys.stderr = weblog
	#sys.stdout = weblog
	
	print "Starting rot application"
	
	#curdir = os.path.dirname(__file__)
	curdir = os.getcwd()
	web.config.debug = config.web_debug
	
	app = web.application(urls, globals())
	
	" ""
	print "setting up session"
	# session setup, make sure to call it only one if in debug mode
	if web.config.get('_session') is None:
		web.config.session_parameters['cookie_name'] = 'rot'
		web.config.session_parameters['cookie_domain'] = None
		web.config.session_parameters['timeout'] = config.session_timeout,
		web.config.session_parameters['ignore_expiry'] = True
		web.config.session_parameters['ignore_change_ip'] = False
		web.config.session_parameters['secret_key'] = config.session_salt
		web.config.session_parameters['expired_message'] = 'Session expired'
	
		temp = tempfile.mkdtemp(dir=curdir+"/"+config.session_dir, prefix='session_')
		web.sess = web.session.Session(
			app, 
			web.session.DiskStore(temp), 
			initializer = session_default
		)
	else:
		web.sess = web.config._session
		try:
			web.sess["pid"]
		except:
			web.sess = session_default
	#web.sess["pid"] += 1
	#print "starting ..."
	
	print "loading hooks"
	app.add_processor(web.loadhook(loadhook))
	app.add_processor(web.unloadhook(unloadhook))
	"" "
	
	web.sess = session_default
	print "Dispatching"
	app.wsgifunc(Log)
"""
if __name__ == "__main__":

	# redirect webserver logs to file
	#weblog = open(config.web_logfile, "ab")
	#sys.stderr = weblog
	#sys.stdout = weblog
	
	curdir = os.path.dirname(__file__)
	curdir=""
	web.config.debug = config.web_debug
	
	app = rot(urls, globals())
	init_session()
	
	app.add_processor(web.loadhook(loadhook))
	app.add_processor(web.unloadhook(unloadhook))
	
	app.run(config.port, "0.0.0.0", Log)
else:
	
	app = web.application(urls, globals())
	init_session()
	
	#web.sess = session_default
	print get_session()
	application = app.wsgifunc()
