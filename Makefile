.PHONY: changelog

all: clean realpath extract uwsgi

SYSTEM = ""
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Linux)
    SYSTEM = "linux"
endif
ifeq ($(UNAME_S),Darwin)
    SYSTEM = "darwin"
endif

uwsgi:
	gcc -v
	tar -C lib -xzf lib/uwsgi-2.0.10.tar.gz
	cd lib/uwsgi-2.0.10 && $(MAKE)
	cp lib/uwsgi-2.0.10/uwsgi bin/uwsgi-$(SYSTEM)
	cd lib/uwsgi-2.0.10 && $(MAKE) plugin.http
	cd lib/uwsgi-2.0.10 && $(MAKE) plugin.python
	cp lib/uwsgi-2.0.10/*.so .

dbshell:
	python -i dshell.py

install-deb:
	#sudo apt-get install uwsgi-plugins-all uwsgi python-opencv python-imaging
	sudo apt-get install build-essential python-dev python-opencv python-imaging

extract:
	./bin/extract.sh
	ln -s static/dist static/bootstrap-3.3.1-dist || true

logview:
	tail -f var/access.log var/application.log

changelog:
	./bin/changelog.py

realpath:
	gcc -o bin/realpath lib/realpath.c

clean:
	find ./ -iname '*~' -exec rm {} \; 2>/dev/null || true
	rm -r var/session_* 2>/dev/null || true
	rm -r var/*.pid 2>/dev/null || true
	find ./ -iname '*.pyc' -exec rm {} \; 2>/dev/null || true
