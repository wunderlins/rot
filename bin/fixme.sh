#!/usr/bin/env bash

f=`./bin/progfiles.sh -v | awk '{print $2}' | grep -v total`
egrep -n "FIXME|TODO" $f > FIXME

