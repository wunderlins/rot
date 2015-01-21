#!/usr/bin/env bash

# drop new tables
mysql -h localhost -uplanoaa -pplanoaa planoaa <<EOT

DROP table IF EXISTS rot_notes;
DROP table IF EXISTS rot_pers;
DROP table IF EXISTS rot_wunsch;
DROP table IF EXISTS rot_erfahrung;
DROP table IF EXISTS rot_rot;
DROP table IF EXISTS rot_rotation;
DROP table IF EXISTS rot_location;
DROP table IF EXISTS rot_group;

EOT
