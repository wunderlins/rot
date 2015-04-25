#!/usr/bin/env bash

basedir="`cd $(dirname $0)/..;pwd`"
cd "$basedir"

basedir=`bin/realpath "$basedir"`

if [[ `hostname` == "sranawebln01" ]]; then
	export cfg_file="config-sranawebln01.py"
else
	export cfg_file="config-dev.py"
fi

. etc/$cfg_file
export basedir
export port
export cfg_file

echo "== Global Config"
echo "Using cfg       : $cfg_file"
echo "basedir         : $basedir"
echo "server          : $server"
echo ""
echo "== Application Config"
echo "port            : $port"
echo "db_user         : $db_user"
echo "db_pass         : $db_pass"
echo "db_name         : $db_name"
echo "db_host         : $db_host"
echo "db_debug        : $db_debug"
echo "web_logfile     : $web_logfile"
echo "app_logfile     : $app_logfile"
echo "sql_logfile     : $sql_logfile"
echo "web_debug       : $web_debug"
echo "session_salt    : $session_salt"
echo "session_timeout : $session_timeout"
echo "session_dir     : $session_dir"

. etc/apache-envvars.sh
echo ""
echo "== Webserver Config"
echo "APACHE_RUN_USER : $APACHE_RUN_USER"
echo "APACHE_RUN_GROUP: $APACHE_RUN_GROUP"
echo "APACHE_PID_FILE : $APACHE_PID_FILE"
echo "APACHE_RUN_DIR  : $APACHE_RUN_DIR"
echo "APACHE_LOCK_DIR : $APACHE_LOCK_DIR"
echo "APACHE_LOG_DIR  : $APACHE_LOG_DIR"
echo "LANG            : LANG"

/usr/sbin/apache2 -d "$basedir" -f etc/apache.conf
echo ""
echo "exit status $?"

