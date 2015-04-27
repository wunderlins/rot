#!/usr/bin/env bash

if [[ `hostname` == "sranawebln01" ]]; then
	export cfg_file="config-sranawebln01.py"
else
	export cfg_file="config-dev.py"
fi

. etc/$cfg_file


echo "Using cfg              : $cfg_file"
echo "Server type            : $server"
echo "Database               : $db_user@$db_host/$db_name"
echo "Debugging              : $web_debug"
echo ""
echo "Webserver Access Log   : $web_logfile"
echo "Application Access Log : $app_logfile"
echo "Database Log           : $sql_logfile"
echo ""
echo "Session Timeout        : $session_timeout # seconds"
echo "Session Directory      : $session_dir/session_*"
echo ""

