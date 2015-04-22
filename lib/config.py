#!/usr/bin/env python

import os, sys
import importlib
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'etc'))

cfg_file = os.getenv("cfg_file")[:-3]
if cfg_file == None:
	print "Please set the environment variable 'cfg_file'"
	sys.exit(1)

#import cfg_file as config
#__import__(cfg_file)
_cfg = importlib.import_module("%s" % cfg_file, '*')

for x in dir(_cfg):
	if str(x)[0:2] == "__":
		continue
	exec(x + " = _cfg." + x)

print "db confg: "  + db_user + "@" + db_host + "/" + db_name

