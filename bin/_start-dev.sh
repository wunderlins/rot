#!/usr/bin/env bash

basedir="`cd $(dirname $0)/..;pwd`"; cd "$basedir"
. lib/setenv.sh

nohup ./httpd.py >> $web_logfile &
