#!/usr/bin/env python

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib', 'web'))
import module

import web
web.config.debug = False
urls = (
    "/count", "count",
    "/reset", "reset"
)
app = web.application(urls, locals())
module.session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'count': 0})

class count:
    def GET(self):
        module.session.count += 1
        return str(module.session.count)

class reset:
    def GET(self):
        module.session.kill()
        return ""

if __name__ == "__main__":
    app.run()
