#!/usr/bin/env bash

basedir="`cd $(dirname $0)/..;pwd`"
cd "$basedir"

if [[ `hostname` == "sranawebln01" ]]; then
	export cfg_file="config-sranawebln01.py"
else
	export cfg_file="config-dev.py"
fi

. etc/$cfg_file

echo "Using cfg: $cfg_file"

uwsgi --plugin python,http --http :9090 --wsgi-file httpd.py
