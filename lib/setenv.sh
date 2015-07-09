#!/usr/bin/env bash

system=""
uname -v | grep "Darwin" >/dev/null 2>&1
if [[ $? == 0 ]]; then system="Darwin"; fi
uname -v | grep "Debian" >/dev/null 2>&1
if [[ $? == 0 ]]; then system="Debian"; fi

export system
export basedir=`dirname ${BASH_SOURCE[0]}`"/.."
basedir=`$basedir/bin/realpath $basedir`

if [[ -n $0 && "$0" != "-bash" ]]; then
	script=`basename $0`
else
	script=""
fi

alias gd='git diff | colordiff | less -R'

if [[ `hostname` == "sranawebln01" ]]; then
	export cfg_file="config-sranawebln01.py"
else
	export cfg_file="config-dev.py"
fi

. $basedir/etc/$cfg_file

PS1="<\[\033[31m\]\h\[\033[0m\]:\[\033[36m\]$server\[\033[0m\]> \[\033[34m\]\W\[\033[0m\]\[\033[37m\]%\[\033[0m\] "

function variables() {
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
	echo "System                 : $system"
	echo ""
}

function start() {
	$basedir/bin/start.sh
}

function stop() {
	$basedir/bin/stop.sh
}

function restart() {
	$basedir/bin/restart.sh
}

function status() {
	variables
	$basedir/bin/status.sh
}

function reload() {
	. $basedir/lib/setenv.sh
}

function rebuild() {
	rm $basedir/static/thumbnails/*.jpg
	$basedir/bin/cache_images.py
}

function grip() {
	if [[ "$1" == "start" ]]; then
		make code
	fi
	
	if [[ "$1" == "stop" ]]; then
		kill -TERM $(lsof -ni TCP | grep 6419 | awk '{print $2}')
	fi

	if [[ "$1" == "status" ]]; then
		proc=$(lsof -ni TCP | grep 6419)
		
		if [[ "$proc" == "" ]]; then
			echo "grip running: false"
			return 0
		else
			echo "grip running: true"
			return 1
		fi
	fi
}

alias bash_help="bash -c 'help'"

function help() {
	cat << EOT
Usage: $script

start
	start daemon

stop
	stop daemon

restart
	restart daemon

status
	check if running.
	Returns 0 if not running, else 1

reload
	reload configuration

rebuild
	clears and rebuilds the thumbnail cache on disk.

NOTE: The bash's builtin help is now available as 'bash_help'.


ENVIRONMENT VARIABLES

EOT

variables
}

#echo $basedir
