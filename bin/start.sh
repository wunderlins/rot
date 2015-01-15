#!/usr/bin/env bash
. config.py

nohup ./httpd.py >> $web_logfile &
