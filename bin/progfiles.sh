#!/usr/bin/env bash

if [[ "$1" == '-v' ]]; then
	wc -l \
		$( \
			find ./ \
				! -path "./lib/*/*" \
				! -path "./static/*/*" \
				! -path "./.git/*" \
				! -path "*~" \
				! -path "*.log" \
				! -path "*.log.*" \
				! -path "*.pid" \
				! -path "*/session_*" \
				! -path "./.*" \
				! -path "./doc/*" \
				! -path "*.csv" \
				! -path "*.ldif" \
				! -path "*data/dev_*.sql" \
				! -path "*data/dev_*.svg" \
				! -path "*ChangeLog" \
				! -path "*.xml" \
				-type f -exec grep -Il . "{}" \;  ;\
			find ./static/rot/app \
				-type f -exec grep -Il . "{}" \;
		)
else
	wc -l \
		$( \
			find ./ \
				! -path "./lib/*/*" \
				! -path "./static/*/*" \
				! -path "./.git/*" \
				! -path "*~" \
				! -path "*.log" \
				! -path "*.log.*" \
				! -path "*.pid" \
				! -path "*/session_*" \
				! -path "./.*" \
				! -path "./doc/*" \
				! -path "*.csv" \
				! -path "*.ldif" \
				! -path "*data/dev_*.sql" \
				! -path "*data/dev_*.svg" \
				! -path "*ChangeLog" \
				! -path "*.xml" \
				-type f -exec grep -Il . "{}" \; ;\
			find ./static/rot/app \
				-type f -exec grep -Il . "{}" \; 
			
		) | tail -n 1 | sed -e 's/ \+//; s/ .*//'
fi

