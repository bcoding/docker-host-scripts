#!/usr/bin/env python
import etcd
import sys

print sys.argv

client = etcd.Client(host='docker2', port=5001)

try:
    name = sys.argv[1]
    port = sys.argv[2]
except IndexError:
    print "NAME PORT"
    exit()

try:
    client.read('/vhosts/' + name)
except KeyError:
    print "vhost not exists"
    exit()

def writeval(key, value):
    client.write('/vhosts/' + '/'.join([name, key]), value)

writeval('port', port)

