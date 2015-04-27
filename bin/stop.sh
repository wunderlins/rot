#!/usr/bin/env bash

basedir="`cd $(dirname $0)/..;pwd`"; cd "$basedir"
. lib/setenv.sh

./bin/stop-$server.sh

# cleanup session data
rm -R var/session_*
