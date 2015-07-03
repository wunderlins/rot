#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
create file cache from images stored in the database. 

this iscript should be run after every backup restore or other database manipulation. Probably a good idea to run this upon starting the server.
"""

import os, sys
#os.chdir(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))

import config, db

if __name__ == "__main__":
	# search all images in the database
	r = db.session.query(db.Person).all()

	for p in r:
		# check if we have a thumbnail
		#print p.pid

		# create if not thumbnail available
		tnpath = "static/thumbnails/%d_thumbnail.jpg" % p.pid
		if not os.path.exists(tnpath):
			fp = open(tnpath, "w")
			fp.write(p.foto_thumbnail)
			fp.close()
			print "%s thumbnail created" % p.pid
		else:
			#print "%s exists" % p.pid
			pass