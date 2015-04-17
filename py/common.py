import os

import etcd
from collections import namedtuple
from docker_utils import get_port

def get_etcd_client():
    return etcd.Client(host='localhost', port=5001)

client = get_etcd_client()

Host = namedtuple('Host', 'ip_addr name ssh_port')
from docker import Client
c = Client(base_url='unix://var/run/docker.sock', version='1.16')

import json
import sys

def get_host(host, container):
    if container:
        return 'b1'
    return host

def flatten_paths(paths, cwd=''):
    cwd = cwd.lstrip('/')
    flattened = {}
    for path, data in paths.items():
        current_path = '%s%s' % (cwd, path)
        if data.get('host') or data.get('container') or data.get('directory'):
            flattened['%s/%s' % (cwd, path + '/')] = data
        else:
            flattened = dict(flatten_paths(data, current_path).items() + flattened.items())
    return flattened


class ApplicationConfig(namedtuple('ApplicationConfig', 'vhost_name docker_container_name docker_container_port')):
    def __new__(cls, **kwargs):
        kwargs['docker_container_port'] = kwargs.get('docker_container_port')
        return super(ApplicationConfig, cls).__new__(cls, **kwargs)

class VirtualHost(namedtuple('VirtualHost', 'name domains flags port host rewrites container paths ip_addr')):
    def __new__(cls, **kwargs):
        kwargs['flags'] = kwargs.get('flags', {})
        kwargs['paths'] = dict([(path.lstrip('/'), {
                        'host': get_host(data.get('host'), data.get('container')),
                        'port': get_port(data.get('container'), data['port']),
                        'setScriptName': data.get('setScriptName', False),
                        'secure': data.get('secure', False),
                        }) for path, data in flatten_paths(kwargs.get('paths', {})).items()])

        for arg in ('rewrites', 'host', 'container'):
            kwargs[arg] = kwargs.get(arg)
	print kwargs
	return super(VirtualHost, cls).__new__(cls, **kwargs)

    @property
    def port(self):
        port = super(VirtualHost, self).port
        return get_port(self.container, port)

    @property
    def host(self):
        host = super(VirtualHost, self).host
        return get_host(host, self.container)

    #@property
    #def domains(self):
    #    return super(VirtualHost, self).domains.split(',')

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
    return result.values()[0]

def get_vm_config():
    with open('/root/config/hosts.json') as f:
        data = json.load(f)
        hosts_data = to_python(client.read('/hosts', recursive=True)).values()
        return [Host(**data) for data in hosts_data]

def get_vhost_config():
    with open('/root/config/nginx_vhosts.json') as f:
        vhosts = []
        for vhost_name, vhost_data in json.load(f).iteritems():
            vhost_data['name'] = vhost_name
            vhosts.append(VirtualHost(**vhost_data))
        return vhosts

def get_applications_config():
    with open('/root/config/applications.json') as f:
        apps = []
        for application_data in json.load(f):
            apps.append(ApplicationConfig(**application_data))
        return apps
