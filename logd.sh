
#!/bin/sh

# PROVIDE: log_captive
# REQUIRE: networking

# move to /usr/local/etc/rc.d
# and use service logd.sh onestart | onestop | onestatus

. /etc/rc.subr

name="log_captive"
rcvar="log_captive_enable"
command="/usr/local/bin/log_parse"
start_cmd="log_captive_start"
stop_cmd="log_captive_stop"
status_cmd="log_captive_status"


log_captive_start() {
    /usr/local/bin/log_parse start
}

log_captive_stop() {
  /usr/local/bin/log_parse stop

}

log_captive_status() {
  /usr/local/bin/log_parse status
}

load_rc_config $name
: ${log_captive_enable:=no}

run_rc_command "$1"
