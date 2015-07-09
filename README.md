Rotationsplanung
====

http://webpy.org/
http://getbootstrap.com/getting-started/

dependencies:
	* build-essential 
	* python-dev 
	* python-opencv 
	* python-ldap 
	* python-imaging
	* (optional) python-pydot # for generating schma graphs
	
On a non debian system, make sure to install gcc (or equivalent) and the above 
python libraries.


Installation
==

First setup the environment:
```bash
$ make extract # extract all archives
$ make realpath # compile our version of realpath
$ . ./lib/setenv.sh # setup environment
```

```bash
Install prerequesites:
<hostname:uwsgi> rot% sudo make install-deb

build uwsgi (current build target debian and osx, requires command line 
xcode tools):
<hostname:uwsgi> rot% make uwsgi

make sure no old session files are left, and backup files are removed
<hostname:uwsgi> rot% make clean

check the config files, change whatever needed then reload the environment
<hostname:uwsgi> rot% reloaod

check current config with
<hostname:uwsgi> rot% status

optional: if the database needs to be created
<hostname:uwsgi> rot% make dbshell # exit with CTRL-D from the prompt

if everythin worked well so far, start the application
<hostname:uwsgi> rot% start # or restart or stop

after the application is started, check access.log and application.log. No 
errors then point a browser at localhost:1975 (or whatever is configured in the
config file). You can find out which config gile is used by issueing the 
following command:
<hostname:uwsgi> rot% status
```
