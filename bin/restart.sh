#!/usr/bin/env bash

basedir="`cd $(dirname $0)/..;pwd`"; cd "$basedir"
. lib/setenv.sh

./bin/stop.sh
sleep 1
./bin/start.sh
