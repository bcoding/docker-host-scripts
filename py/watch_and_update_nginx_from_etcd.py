#!/usr/bin/env python

import common
import etcd
import urllib3

PUBLIC_ADDRESS = '1.2.3.4'
CERT_DIR = '/root/certs'

import subprocess
from update_nginx_vhosts import update_vhosts

def update_nginx_from_etcd():
    vm_map = dict([(host.name, {'local_address': host.ip_addr}) for host in common.get_vm_config()])
    
    def create_certificates(domains):
        format_args = {'cert_dir': CERT_DIR}
    
        import os.path
        if not os.path.isfile(os.path.join(CERT_DIR, 'acmeCA.key.deleteme')):
            commands = """openssl rsa -in %(cert_dir)s/acmeCA.key -out %(cert_dir)s/acmeCA.key.deleteme""" % format_args
            for command in [cmd for cmd in commands.split("\n") if cmd]:
                subprocess.call([arg for arg in command.split(" ") if arg])
    
        for domain in domains:
            create_certificate(domain)
    
    def create_certificate(domain):
        format_args = {'domain': domain,
                       'cert_dir': CERT_DIR}
        
        commands = """
        openssl genrsa -out %(cert_dir)s/%(domain)s.key 2048
        openssl req -new -key %(cert_dir)s/%(domain)s.key -out %(cert_dir)s/%(domain)s.csr  -subj /C=DE/ST=Niedersachsen/L=Osnabrueck/O=OPS/CN=%(domain)s
        openssl x509 -req -in %(cert_dir)s/%(domain)s.csr -CA %(cert_dir)s/acmeCA.pem -CAkey %(cert_dir)s/acmeCA.key.deleteme -CAcreateserial -out %(cert_dir)s/%(domain)s.crt -days 500
        rm %(cert_dir)s/%(domain)s.csr""" % format_args
        
        for command in [cmd for cmd in commands.split("\n") if cmd]:
            print command.split(" ")
            subprocess.call([arg for arg in command.split(" ") if arg])
    
    # create_certificates([host.domains[0] for host in common.get_vhost_config()])

    update_vhosts(common.get_vhost_config())
    
client = common.get_etcd_client();

while True:
    try:
        client.read('/', recursive=True, wait=True)
        update_nginx_from_etcd()
        subprocess.call([arg for arg in "service nginx reload".split(" ") if arg])
        # subprocess.call([arg for arg in "/bin/sh /var/lib/libvirt/shares/docker2/fix_permissions.sh".split(" ") if arg])
    except urllib3.exceptions.TimeoutError:
        continue
    except:
        pass
