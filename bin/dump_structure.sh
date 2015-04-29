#!/usr/bin/env bash

basedir="`cd $(dirname $0)/..;pwd`"; cd "$basedir"
. lib/setenv.sh

mysqldump -d -h $db_host -u $db_user -p$db_pass $db_name
