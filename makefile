
DIR_BIN = /usr/local/bin
DIR_RC = /usr/local/etc/rc.d

all:
	@ echo "Usage 'make install'"

install:
	cp parse_filter_captive.py $(DIR_BIN)/
	chmod +x $(DIR_BIN)/parse_filter_captive.py

	cp log_parse $(DIR_BIN)/
	chmod +x $(DIR_BIN)/log_parse

	cp logd $(DIR_RC)/
	chmod +x $(DIR_RC)/logd

	@ echo "Instaled, now 'make start' to start process" 

uninstall:
	rm $(DIR_BIN)/parse_filter_captive.py
	rm $(DIR_BIN)/log_parse
	rm $(DIR_RC)/logd

start:
	$(DIR_RC)/logd start

stop:
	$(DIR_RC)/logd stop

status:
	$(DIR_RC)/logd status
