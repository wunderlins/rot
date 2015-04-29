dbshell:
	python -i dshell.py

install-deb:
	sudo apt-get install uwsgi-plugins-all uwsgi python-opencv python-imaging

install:
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
