#!/usr/bin/env python

import os
import common

PUBLIC_ADDRESS = '1.2.3.4'

for name,ip,port in common.get_vm_config():
    format_args = {'public_address': PUBLIC_ADDRESS, 'public_port': port, 'local_port': 22, 'local_address': ip}
    print "iptables -t nat -I PREROUTING -p tcp -d %(public_address)s --dport %(public_port)s -j DNAT --to-destination %(local_address)s:%(local_port)s" % format_args


print "iptables -I FORWARD -m state -d 10.0.0.0/24 --state NEW,RELATED,ESTABLISHED -j ACCEPT"
