#!/bin/sh
### BEGIN INIT INFO
# Provides:          swiperproxy
# Required-Start:    $named $network $remote_fs $syslog
# Required-Stop:     $named $network $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Starts, stops, restarts or returns status of
#                    SwiperProxy.
# Description:       An init script to start, stop or restart the
#                    SwiperProxy HTTP/HTTPS proxy, or return the
#                    current status.
### END INIT INFO

# Author: Patrick Godschalk <argure@donttrustrobots.nl>

DIR=/opt/SwiperProxy/swiperproxy
DESC="HTTP/HTTPS web proxy"
NAME=swiperproxy
DAEMON=$DIR/Proxy.py
DAEMON_OPTS="-c /etc/swiperproxy/proxy.conf"
DAEMON_USER=swiperproxy
PIDFILE=/var/run/swiperproxy.pid

# Read default configuration variable file if it is present
[ -r /etc/default/$NAME ] && . /etc/default/$NAME

# Exit if the package is not installed
[ -x "$DAEMON" ] || exit 0

# Define LSB log_* functions.
# Depend on lsb-base (>= 3.2-14) to ensure that this file is present
# and status_of_proc is working.
. /lib/lsb/init-functions

do_start()
{
	log_daemon_msg "Starting system $NAME daemon"
	start-stop-daemon --start --background --pidfile $PIDFILE --make-pidfile --user $DAEMON_USER --chuid $DAEMON_USER --startas $DAEMON -- $DAEMON_OPTS
	log_end_msg $?
}

do_stop()
{
	log_daemon_msg "Starting system $NAME daemon"
	start-stop-daemon --stop --pidfile $PIDFILE --retry 10
	log_end_msg $?
}

case "$1" in
  start|stop)
	do_${1}
	;;
  restart|force-reload)
	do_stop
	do_start
	;;
  status)
	status_of_proc "$NAME" "$DAEMON" && exit 0 || exit $?
	;;
  *)
	echo "Usage: $SCRIPTNAME {start|stop|status|restart|force-reload}"
	exit 1
	;;
esac

exit 0
