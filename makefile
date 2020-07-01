
DIR_BIN = /usr/local/bin
DIR_RC = /usr/local/etc/rc.d

PHONY: install uninstall

install:
	cp parse_filter_captive.py $(DIR_BIN)/
	chmod +x $(DIR_BIN)/parse_filter_captive.py

	cp log_parse $(DIR_BIN)/
	chmod +x $(DIR_BIN)/log_parse

	cp logd $(DIR_RC)/
	chmod +x $(DIR_RC)/logd

uninstall:
	rm $(DIR_BIN)/parse_filter_captive.py
	rm $(DIR_BIN)/log_parse
	rm $(DIR_RC)/logd
