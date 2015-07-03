#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'web'))

from web import session

class WebSession(session.Session):
	def get_data(self):
		return self._data