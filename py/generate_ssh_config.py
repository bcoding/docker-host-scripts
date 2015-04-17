#!/usr/bin/env python

import common
import sys

for name,ip,port in common.get_vm_config():
    format_args = {'public_port': port, 'name': name, 'username': sys.argv[1]}
    print """
Host %(name)s
    HostName asdfasdf
    User %(username)s
    Port %(public_port)s
""" % format_args
