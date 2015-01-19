#!/usr/bin/env python

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib', 'web'))

import web
import re
import base64
import tempfile

urls = (
    '/','Index',
    '/login','Login'
)

session_default = {
	"selected_pid": 0,
	"pid": 0,
	"user": None
}

allowed = (
    ('jon','pass1'),
    ('tom','pass2')
)

app = web.application(urls,globals())

# session setup, make sure to call it only one if in debug mode
if web.config.get('_session') is None:
	web.config.session_parameters['cookie_name'] = 'rot'
	web.config.session_parameters['cookie_domain'] = None
	web.config.session_parameters['timeout'] = 6400,
	web.config.session_parameters['ignore_expiry'] = False
	web.config.session_parameters['ignore_change_ip'] = False
	web.config.session_parameters['secret_key'] = "asd asdasd sdsd"
	web.config.session_parameters['expired_message'] = 'Session expired'

	temp = tempfile.mkdtemp(dir="../var", prefix='session_')
	session = web.session.Session(
		app, 
		web.session.DiskStore(temp), 
		initializer = session_default
	)
else:
	session = web.config._session

class Index:
	def GET(self):
		global session
		try:
			session["user"]
		except:
			session = session_default
		
		auth = web.ctx.env.get('HTTP_AUTHORIZATION')
		if auth is not None:
			session["user"] = None
			auth = re.sub('^Basic ','',auth)
			username,password = base64.decodestring(auth).split(':')
			if (username,password) in allowed:
				session["user"] = username
		
		if session["user"] == None:
			web.header('WWW-Authenticate','Basic realm="Auth example"')
			web.ctx.status = '401 Unauthorized'
			return
		
		return "logged in as " + session["user"]
		

"""
class Index:
    def GET(self):
        if web.ctx.env.get('HTTP_AUTHORIZATION') is not None:
            return web.ctx.env
        else:
		      auth = web.ctx.env.get('HTTP_AUTHORIZATION')
		      authreq = False
		      if auth is None:
		          authreq = True
		      else:
		          auth = re.sub('^Basic ','',auth)
		          username,password = base64.decodestring(auth).split(':')
		          if (username,password) in allowed:
		              raise web.seeother('/')
		          else:
		              authreq = True
		      if authreq:
		          web.header('WWW-Authenticate','Basic realm="Auth example"')
		          web.ctx.status = '401 Unauthorized'
		          return
class Login:
    def GET(self):
        auth = web.ctx.env.get('HTTP_AUTHORIZATION')
        authreq = False
        if auth is None:
            authreq = True
        else:
            auth = re.sub('^Basic ','',auth)
            username,password = base64.decodestring(auth).split(':')
            if (username,password) in allowed:
                raise web.seeother('/')
            else:
                authreq = True
        if authreq:
            web.header('WWW-Authenticate','Basic realm="Auth example"')
            web.ctx.status = '401 Unauthorized'
            return
"""

if __name__=='__main__':
    app.run()
