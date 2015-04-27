basedir="`cd $(dirname $0)/..;pwd`"

export APACHE_RUN_USER=$USER
export APACHE_RUN_GROUP=$USER
export APACHE_PID_FILE=$basedir/apache.pid
export APACHE_RUN_DIR=$basedir/var/
export APACHE_LOCK_DIR=$basedir/var/
# Only /var/log/apache2 is handled by /etc/logrotate.d/apache2.
export APACHE_LOG_DIR=$basedir/var/

## The locale used by some modules like mod_dav
export LANG=C
## Uncomment the following line to use the system default locale instead:
#. /etc/default/locale

export LANG

## The command to get the status for 'apache2ctl status'.
## Some packages providing 'www-browser' need '--dump' instead of '-dump'.
#export APACHE_LYNX='www-browser -dump'

## If you need a higher file descriptor limit, uncomment and adjust the
## following line (default is 8192):
#APACHE_ULIMIT_MAX_FILES='ulimit -n 65536'


## If you would like to pass arguments to the web server, add them below
## to the APACHE_ARGUMENTS environment.
#export APACHE_ARGUMENTS=''

