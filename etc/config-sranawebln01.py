# NOTE: make syntax bash compatible!
#       no spaces between name = value, like this: name=value

server="uwsgi" # uwsgi|dev|apache (apache is not workign yet)

port=1975

db_user="planoaa"
db_pass="planoaa"
db_name="planoaa"
db_host="srsqlln01.uhbs.ch"

db_debug=False

web_logfile="var/access.log"
app_logfile="var/application.log"
sql_logfile="var/sql.log"

web_debug=True

session_salt="26fe3630-a4af-45bd-b063-3a9917c8cb97"
session_timeout=86400 #24 * 60 * 60, # 24 hours   in seconds
session_dir='var'
