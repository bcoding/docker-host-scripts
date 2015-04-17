#!/usr/bin/env python

import common
import sys

for name,ip,port in common.get_vm_config():
    format_args = {'public_port': port,
                   'name': name,
                   'local_address': ip
                   }
    print "%(local_address)s\t%(name)s %(name)s.acme.intern" % format_args
