
DIR_BIN = /usr/local/bin
DIR_RC = /usr/local/etc/rc.d

all:
	@ echo "Usage 'make install'"

install:
	cp parse_filter_captive.py $(DIR_BIN)/
	chmod +x $(DIR_BIN)/parse_filter_captive.py

	cp log_parse $(DIR_BIN)/
	chmod +x $(DIR_BIN)/log_parse

	cp logd.sh $(DIR_RC)/
	chmod +x $(DIR_RC)/logd.sh

	@ echo "\nInstaled, now 'make start' to start process"
	@ echo  "process already startup on boot system"

uninstall:
	rm $(DIR_BIN)/parse_filter_captive.py
	rm $(DIR_BIN)/log_parse
	rm $(DIR_RC)/logd

start:
	$(DIR_RC)/logd.sh onestart

stop:
	$(DIR_RC)/logd.sh onestop

status:
	$(DIR_RC)/logd.sh onestatus

debug:
	(/usr/bin/tail -f -n0 /var/log/filter.log.txt  & echo $! > teste.pid) | \
	/usr/local/bin/python3.6 /usr/local/bin/parse_filter_captive.py

clean_debug:
	rm `cat teste.pid`
