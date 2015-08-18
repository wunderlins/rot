#!/usr/bin/env bash

# 2.0.11 doesn't seem to write the proper pid into the pid file
#pids=`ps aux | grep rot.pid | grep -v grep | awk '{print $2}'`
#
#if [[ "$pids" != "" ]]; then
#	for p in $pids; do
#		kill -TERM $p
#	done
#fi

# alternative method to stop the process is by killing all programs which are 
# listening on the configured port. be careful when changing the port in the 
# config file

basedir="`cd $(dirname $0)/..;pwd`"; cd "$basedir"
. lib/setenv.sh

if [[ $system == "Darwin" ]]; then
	kill -9 `ps aux | grep rot.pid | awk '{print $2}'`
else
	kill -9 `lsof -ni TCP | grep $port | awk '{print $2}'`
fi