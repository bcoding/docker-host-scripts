from docker import Client
c = Client(base_url='unix://var/run/docker.sock', version='1.16')

import json
import sys

def get_port(container, port):
    if container:
        ports = c.inspect_container(container)['NetworkSettings']['Ports'].keys()
        return int(ports[0].split('/')[0])
    return port

class ContainerConfig():
    pass

def get_config(container):
    config = ContainerConfig()
    data = c.inspect_container(container)
    ports = data['NetworkSettings']['Ports'].keys()

    config.port = int(ports[0].split('/')[0])
    config.ip_addr = data['NetworkSettings']['IPAddress']
    return config

#def get_vm_config():
#    vm_map = dict([(host.name, {'local_address': host.ip_addr}) for host in common.get_vm_config()])
#    hosts_data = to_python(client.read('/hosts', recursive=True)).values()
#    return [Host(**data) for data in hosts_data]
#
#print json.dumps(c.containers())
