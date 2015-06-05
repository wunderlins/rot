#!/usr/bin/env bash

echo "personalnr;name;count;pid;pidp;kuerzel"
echo "" > merge.sql
while read l; do 
	#echo $l; 
	nr=`echo $l | cut -d';' -f5`
	name=`echo $l | cut -d';' -f2 | sed -e 's/ .*//; s/'\''/%/'`
	echo -en "$nr;$name;"
	
	sql="SELECT pid, pidp, kuerzel FROM personal WHERE name LIKE '%--%'"
	
	
	res=`echo "$sql" | sed -e 's/--/'$name'/' | mysql -B --skip-column-names --delimiter ';' -h srsqlln01.uhbs.ch -uplanoaa -pplanoaa planoaa | sed -e 's/	/;/g'`
	numl=`echo "$res" | wc -l`
	echo -en "$numl;"
	pid=""
	if [[ "$numl" == "1" ]]; then
		echo -en "$res"
		pid=`echo "$res" | cut -d';' -f1`
	else
		echo -en ";;"
	fi
	echo ""
	
	if [[ "$pid" != "" ]]; then
		echo "UPDATE personal SET personalid=$nr WHERE pid=$pid; -- $res" >> merge.sql
	fi
	
done < personalnummern2.csv


while read l; do
	nr=`echo "$l" | cut -d';' -f1`
	pid=`echo "$l" | cut -d';' -f4`
	echo "UPDATE personal SET personalid=$nr WHERE pid=$pid;" >> merge.sql
done < manual.csv
