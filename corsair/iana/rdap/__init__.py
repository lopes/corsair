import urllib.request
import re

from urllib.parse import urlencode
from json import loads
from socket import timeout
from ssl import _create_unverified_context
from ipaddress import ip_network, ip_address

from corsair import *


re_ipv6 = re.compile(r'^(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))$')
re_ipv4 = re.compile(r'^((2([0-4][0-9]|5[0-5])|1?[0-9]?[0-9])\.){3}(2([0-4][0-9]|5[0-5])|1?[0-9]?[0-9])$')
re_domain = re.compile(r'^[a-zA-Z0-9]([a-zA-Z0-9\.-_])+([a-zA-Z0-9]+)$')
re_asn = re.compile(r'^[0-9]+$')


class Api(object):
    def __init__(self, base_url='https://data.iana.org/rdap/', 
        tls_verify=True):
        self.base_url = base_url
        self.tls_verify = tls_verify

        self.asn = self.parse_asn('asn.json')
        self.ip = self.merge_ips(self.parse_ip('ipv4.json'), 
            self.parse_ip('ipv6.json'))
        self.dns = self.parse_dns('dns.json')

        self.ip = Endpoint((self.ip, self.tls_verify), 'ip')
        self.domain = Endpoint((self.dns, self.tls_verify), 'domain')
        self.autnum = Endpoint((self.asn, self.tls_verify), 'autnum')
    
    def parse_asn(self, _endpoint):
        parsed = dict()
        req = Request(make_url(self.base_url, _endpoint, ''), self.tls_verify)
        res = loads(req.get().read())
        for service in res['services']:
            parsed.update({service[1][0]: list()})
            for r in service[0]:
                s = r.split('-')
                if len(s) > 1:
                    parsed[service[1][0]].append(range(int(s[0]), int(s[1])+1))
                else:
                    parsed[service[1][0]].append(range(int(s[0]), int(s[0])+1))
        return parsed
    
    def parse_ip(self, _endpoint):
        parsed = dict()
        req = Request(make_url(self.base_url, _endpoint, ''), self.tls_verify)
        res = loads(req.get().read())
        for service in res['services']:
            parsed.update({service[1][0]: list()})
            for r in service[0]:
                parsed[service[1][0]].append(ip_network(r))
        return parsed
    
    def parse_dns(self, _endpoint):
        parsed = dict()
        req = Request(make_url(self.base_url, _endpoint, ''), self.tls_verify)
        res = loads(req.get().read())
        for service in res['services']:
            parsed.update({service[1][0]: list()})
            for r in service[0]:
                parsed[service[1][0]].append(r)
        return parsed
    
    def merge_ips(self, ipv4, ipv6):
        merged = ipv4
        for k,v in ipv6.items():
            if k in merged:
                merged[k].extend(v)
        return merged


class Endpoint(object):
    def __init__(self, api, endpoint):
        self.bootstrap = api[0]
        self.tls_verify = api[1]
        self.endpoint = endpoint
        self.resource = ''
        self.base_url = ''
    
    def read(self, _resource, **filters):
        if re_ipv4.match(_resource) or re_ipv6.match(_resource):
            self.base_url = self.get_base_url(ip_address(_resource))
        elif re_asn.match(_resource):
            self.base_url = self.get_base_url(int(_resource))
        elif re_domain.match(_resource):
            self.base_url = self.get_base_url(_resource.split('.')[-1])
        self.resource = _resource
        req = Request(make_url(self.base_url, self.endpoint, self.resource), 
            self.tls_verify)
        res = req.get(**filters)
        return loads(res.read())
    
    def get_base_url(self, _resource):
        for k,v in self.bootstrap.items():
            for r in v:
                if _resource in r:
                    return k


class Request(object):
    def __init__(self, url, tls_verify):
        self.url = url
        self.timeout = TIMEOUT
        self.context = None if tls_verify else _create_unverified_context()
        self.headers = {
            'Content-Type': 'application/json'
        }
    
    def get(self, **filters):
        url = f'{self.url}?{urlencode(filters)}' if filters else self.url
        req = urllib.request.Request(url, headers=self.headers, method='GET')
        return urllib.request.urlopen(req, timeout=self.timeout, 
            context=self.context)
