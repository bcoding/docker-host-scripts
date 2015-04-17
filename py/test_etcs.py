#!/usr/bin/env python
import etcd
import json

client = etcd.Client(host='docker2', port=5001)
v = open("vhosts.json").read()

try:
    client.get('/vhosts')
except KeyError:
    client.write('/vhosts', None, dir=True)

for vhost in json.loads(v):
    name = vhost['name']
    host = vhost['host']
    port = vhost['port']
    domains = vhost['domains']
    flags = vhost['flags']

    try:
        client.read('/vhosts/' + name)
    except KeyError:
        client.write('/vhosts/' + name, None, dir=True)

    def writeval(key, value):
        client.write('/vhosts/' + '/'.join([name, key]), value)

    writeval('name', name)
    writeval('host', host)
    writeval('port', port)
    writeval('domains', ",".join(domains))

    try:
        client.read('/vhosts/' + '/'.join([name, 'flags']))
        client.delete('/vhosts/' + '/'.join([name, 'flags']), dir=True, recursive=True)
    except KeyError:
        pass

    client.write('/vhosts/' + '/'.join([name, 'flags']), None, dir=True)
    for flag, value in flags.items():
        client.write('/vhosts/' + '/'.join([name, 'flags', flag]), value if not type(value) == bool else ('1' if value else '0'))

hosts = ['docker2:10.0.0.7:22206',
'16bars:10.0.0.9:22205',
'16bars_staging:10.0.0.10:22208',
'bikl:10.0.0.8:22207',
'host1:178.63.42.75:22']

client.delete('/hosts', dir=True, recursive=True)

for name,ip_addr,ssh_port in [tuple(host.split(':')) for host in hosts]:

    try:
        client.read('/hosts/' + name)
    except KeyError:
        client.write('/hosts/' + name, None, dir=True)

    def writeval(key, value):
        client.write('/hosts/' + '/'.join([name, key]), value)

    writeval('name', name)
    writeval('ssh_port', port)
    writeval('ip_addr', ip_addr)

def to_python(etcd_dir):
    result = {}
    for child in etcd_dir.children:
        path = child.key.split('/')[1:]
        if not child.dir:
            path = path[:-1]
        container = result
        for step in path:
            if not step in container:
                container[step] = {}
            container = container[step]
        if not child.dir:
            container[child.key.split('/')[-1]] = child.value
    return result

print to_python(client.read('/vhosts', recursive=True))

print to_python(client.read('/hosts', recursive=True))
