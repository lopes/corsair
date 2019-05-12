import urllib.request

from urllib.parse import urlencode
from json import loads
from socket import timeout
from ssl import _create_unverified_context
from ipaddress import ip_network

from corsair import *


class Api(object):
    def __init__(self, tls_verify=True):
        self.tls_verify = tls_verify
        self.root = 'https://data.iana.org/rdap/'
        self.asn = self.parse_asn()
        self.ipv4 = self.parse_ip()
        self.ipv6 = self.parse_ip('ipv6.json')
        self.credentials = (self.root, self.tls_verify)

        self.domain = Endpoint(self.credentials, 'domain')
        self.autnum = Endpoint(self.credentials, 'autnum')
        self.entity = Endpoint(self.credentials, 'entity')
        self.ip = Endpoint(self.credentials, 'ip')
    
    def parse_asn(self, resource='asn.json'):
        asn = dict()
        req = Request(f'{self.root}/{resource}', self.tls_verify)
        res = loads(req.get().read())
        for service in res['services']:
            asn.update({service[1][0]: list()})
            for r in service[0]:
                s = r.split('-')
                if len(s) > 1:
                    asn[service[1][0]].append(range(int(s[0]), int(s[1])+1))
                else:
                    asn[service[1][0]].append(range(int(s[0]), int(s[0])+1))
        return asn
    
    def parse_ip(self, resource='ipv4.json'):
        ip = dict()
        req = Request(f'{self.root}/{resource}', self.tls_verify)
        res = loads(req.get().read())
        for service in res['services']:
            ip.update({service[1][0]: list()})
            for r in service[0]:
                ip[service[1][0]].append(ip_network(r))
        return ip


class Endpoint(object):
    def __init__(self, credentials, endpoint):
        pass


class Request(object):
    def __init__(self, url, tls_verify):
        self.url = url
        self.timeout = TIMEOUT
        self.context = None if tls_verify else _create_unverified_context()
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    
    def get(self, **filters):
        url = f'{self.url}?{urlencode(filters)}' if filters else self.url
        req = urllib.request.Request(url, headers=self.headers, method='GET')
        return urllib.request.urlopen(req, timeout=self.timeout, context=self.context)
