#!/usr/bin/env bash

. etc/dbconfig.sh

# import existing data from file
mysql -h $host -u$user -p$pass $db < data/planoaa.sql
