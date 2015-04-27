#!/usr/bin/env bash

basedir="`cd $(dirname $0)/..;pwd`"; cd "$basedir"
. lib/setenv.sh

uwsgi --plugin python,http \
      --http :$port \
      --wsgi-file httpd.py \
      --static-map /static=static/ \
      --pidfile var/uwsgi.pid \
      --logto $web_logfile