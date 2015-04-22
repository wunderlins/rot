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
nohup ./httpd.py >> $web_logfile &
