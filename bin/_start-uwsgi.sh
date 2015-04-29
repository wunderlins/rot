#!/usr/bin/env bash

basedir="`cd $(dirname $0)/..;pwd`"; cd "$basedir"
. lib/setenv.sh

bin=uwsgi
if [[ "$system" == "Darwin" ]]; then
	bin=$basedir/bin/uwsgi-osx
fi

$bin  --plugin python,http \
      --http :$port \
      --wsgi-file httpd.py \
      --static-map /static=static/ \
      --pidfile var/rot.pid \
      --daemonize $web_logfile \
      --workers 5
#      --logto $web_logfile \
#      --daemonize2 var/uwsgi.log
