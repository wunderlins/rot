#!/usr/bin/env bash

basedir="`cd $(dirname $0)/..;pwd`"; cd "$basedir"
. lib/setenv.sh

basedir=`bin/realpath "$basedir"`

pids=`ps aux | grep apache | grep $basedir | cut -d' ' -f8`
kill -TERM `cat $basedir/ar/apache2/apache.pid` $pids 


