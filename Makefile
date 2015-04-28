dbshell:
	python -i dshell.py

install:
	./bin/extract.sh
	cd static/
	ln -s dist bootstrap-3.3.1-dist || true
	sudo apt-get install uwsgi-plugins-all uwsgi python-opencv python-imaging

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
