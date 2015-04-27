#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
#os.chdir(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib', 'web'))
#sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

import web, config
from webctx import *

session_default = {
	"selected_pid": 0,
	"pid": 0,
	"user": None
}

app = web.application(urls, globals())
web.sess = session_default
print web.sess
application = app.wsgifunc()
