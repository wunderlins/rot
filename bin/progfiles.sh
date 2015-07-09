#!/usr/bin/env bash

wc -l \
	$( \
		find ./ \
			! -path "./lib/*/*" \
			! -path "./static/*/*" \
			! -path "./.git/*" \
			! -path "*~" \
			! -path "*.log" \
			! -path "*.pid" \
			! -path "./.*" \
			! -path "./doc/*" \
			! -path "*.csv" \
			! -path "*.ldif" \
			! -path "*data/dev_*.sql" \
			! -path "*data/dev_*.svg" \
			! -path "*ChangeLog" \
			! -path "*.xml" \
			-type f -exec grep -Il . "{}" \; 
	) | tail -n 1 | sed -e 's/ \+//; s/ .*//'
