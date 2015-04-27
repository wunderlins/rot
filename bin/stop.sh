#!/usr/bin/env bash

basedir="`cd $(dirname $0)/..;pwd`"; cd "$basedir"
. lib/setenv.sh

./bin/_stop-$server.sh

# cleanup session data
rm -R var/session_* 2>/dev/null
