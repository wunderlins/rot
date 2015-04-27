#!/usr/bin/env bash

pids=`ps aux | grep httpd.py | grep -v grep | awk '{print $2}'`

if [[ "$pids" != "" ]]; then
	for p in $pids; do
		kill -TERM $p
	done
fi


