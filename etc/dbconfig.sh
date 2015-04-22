if [[ `hosntmane` == "sranawebln01" ]]; then
	export cfg_file="config-sranawebln01.py"
else
	export cfg_file="config-dev.py"
fi

. etc/$cfg_file

user="$db_user"
pass="$db_pass"
host="$db_host"
db="$db_name"
