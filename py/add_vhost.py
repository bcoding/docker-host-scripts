#!/usr/bin/env python
import etcd
import json

import sys

print sys.argv

client = etcd.Client(host='docker2', port=5001)

try:
    name = sys.argv[1]
    host = sys.argv[2]
    port = sys.argv[3]
    domain = sys.argv[4]
except IndexError:
    print "NAME HOST PORT DOMAIN"
    exit()

try:
    client.read('/vhosts/' + name)
    print "host exists"
    exit()
except KeyError:
    client.write('/vhosts/' + name, None, dir=True)

def writeval(key, value):
    client.write('/vhosts/' + '/'.join([name, key]), value)

writeval('name', name)
writeval('host', host)
writeval('port', port)
writeval('domains', domain)

