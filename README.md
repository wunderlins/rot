Rotationsplanung
====

http://webpy.org/
http://getbootstrap.com/getting-started/

dependencies:
	* build-essential 
	* python-dev 
	* python-opencv 
	* python-imaging
	* (optional) python-pydot # for generating schma graphs
	
On a non debian system, make sure to install gcc (or equivalent) and the above 
python libraries.


Installation
==

First setup the environment:
$ . ./lib/setenv.sh

Install prerequesites:
<hostname:uwsgi> rot% make install-deb

unpack all custom libraries an packages:
<hostname:uwsgi> rot% make install

if this system has not realpath builtin or binary, build it (check with 
realpath if it exists):
<hostname:uwsgi> rot% make realpath

build uwsgi (current build target debian and osx, requires command line 
xcode tools):
<hostname:uwsgi> rot% make uwsgi

make sure no old session files are left
<hostname:uwsgi> rot% make clean

check the config files, change whatever needed then reload the environment
<hostname:uwsgi> rot% reloaod

check current config with
<hostname:uwsgi> rot% status

optional: if the database needs to be created
<hostname:uwsgi> rot% make dbshell # exit with CTRL-D from the prompt

if everythin worked well so far, start the application
<hostname:uwsgi> rot% start # or restart or stop
