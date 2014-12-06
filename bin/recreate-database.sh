#!/usr/bin/env bash

# import existing data from file
mysql -h localhost -uplanoaa -pplanoaa planoaa < data/planoaa.sql
