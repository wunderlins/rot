#!/usr/bin/env bash

# setup environment
basedir="`cd $(dirname $0)/..;pwd`"; cd "$basedir"
. lib/setenv.sh

# precache images from database
./bin/cache_images.py &

# start configured server
./bin/_start-$server.sh
