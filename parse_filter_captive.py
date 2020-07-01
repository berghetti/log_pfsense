#!/usr/bin/python3.6

"""
Usage example
tail -F -n0 filter.log | ./parse.py
tail -F -n0 filter.log | ./parse.py | logger ...

# 1 - listening file filters firewall
# 2 - parse data and associate with user (if there is)
# 3 - send log to a remote syslog

tail -f -n0 /var/log/filter.log.txt | \
python3.6 /usr/local/bin/parse_filter_captive.py | \
logger -t captive_pfsense -h "ip_syslog_sv" -p "port_syslog_sv" -4
"""

import sys

# change to file log right
captive = r"/var/log/portalauth.log.txt"

line_parsed = dict()

offset = 0

#     line_parsed['mes'],
#     line_parsed['dia'],
#     line_parsed['time'],
#     line_parsed['ip_src'],
#     line_parsed['port_src'],
#     line_parsed['ip_dst'],
#     line_parsed['port_dst'],
#     line_parsed['iface'],
#     line_parsed['direction'],
#     line_parsed['proto'],   # tcp | udp | icmp ...
#     line_parsed['lenght'],  # len frame
#     line_parsed['action'],  # block | pass
#     line_parsed['user'],
#     line_parsed['mac_address'],

key_print = ['mes', 'dia', 'time', 'ip_src', 'port_src', 'ip_dst', 'port_dst',
        'iface', 'direction', 'proto', 'lenght', 'action', 'mac', 'user']

def main():
    # with open(filter, "r") as filter_f:
        # for line_filter in filter_f:
    for line_filter in sys.stdin:
            line_filter = line_filter.rstrip()
            # test blanck lines
            if not line_filter:
                continue

            if not 'filterlog' in line_filter:
                continue

            data_filter = line_filter.split(',')

            #remove extra space
            timestamp = ' '.join( data_filter[0].split() )
            line_parsed['mes'] = timestamp.split(' ')[0]
            line_parsed['dia'] = timestamp.split(' ')[1]
            line_parsed['time'] = timestamp.split(' ')[2]

            line_parsed['iface'] = data_filter[4]
            line_parsed['action'] = data_filter[6]
            line_parsed['direction'] = data_filter[7]
            line_parsed['ip_version'] = data_filter[8]

            # # ipv4
            if line_parsed['ip_version'] == "4":
                line_parsed['proto_id'] = data_filter[15]
                line_parsed['proto'] = data_filter[16]
                line_parsed['lenght'] = data_filter[17]
                line_parsed['ip_src'] = data_filter[18]
                line_parsed['ip_dst'] = data_filter[19]
                offset = 19
            # # ipv6
            elif line_parsed['ip_version'] == "6":
                line_parsed['proto'] = data_filter[12]
                line_parsed['proto_id'] = data_filter[13]
                line_parsed['lenght'] = data_filter[14]
                line_parsed['ip_src'] = data_filter[15]
                line_parsed['ip_dst'] = data_filter[16]
                offset = 16
            else:
                # error, packet invalid
                continue

            # TCP or UDP
            if line_parsed['proto_id'] == "6" or line_parsed['proto_id'] == "17":
                offset += 1
                line_parsed['port_src'] = data_filter[offset]
                offset += 1
                line_parsed['port_dst']   = data_filter[offset]
            else:
                line_parsed['port_src'] = ""
                line_parsed['port_dst'] = ""


            line_parsed['user'] = ""
            line_parsed['mac_address'] = ""
            try:
                with open(captive, "r") as captive_f:
                    # last ocorrency of ip
                    for line_captive in reversed(list(captive_f)):
                        line_captive = line_captive.strip()
                        if not line_captive:
                            continue

                        # filter only log of auth
                        if not 'logportalauth' in line_captive:
                            continue

                        data_captive = line_captive.split(':')
                        user = data_captive[5].split(',')[0]
                        mac = line_captive.split(' ')[10]
                        mac = mac.strip(',')

                        if line_parsed['ip_src'] in line_captive or line_parsed['ip_dst'] in line_captive:
                            if 'ACCEPT' in line_captive:
                                line_parsed['user'] = "ifms\\" + user.strip()
                                line_parsed['mac_address'] = mac

                            break
            except:
                pass


            for key in key_print:
                if key in line_parsed.keys() and line_parsed[key]:
                    print( line_parsed[key], end = ' ' )

            print(flush = True)

if __name__ == '__main__':
    try:
        main()
    except:
        pass
