import urllib.request

from urllib.parse import urlencode
from json import loads, dumps
from socket import timeout
from ssl import _create_unverified_context

from corsair import *


class Api(object):
    def __init__(self, base_url, auth, tls_verify=True):
        self.base_url = base_url if base_url[-1] != '/' else base_url[:-1]
        self.auth = auth
        self.tls_verify = tls_verify
        self.credentials = (self.base_url, self.auth, self.tls_verify)

        self.circuits = Endpoint(self.credentials, 'circuits')
        self.dcim = Endpoint(self.credentials, 'dcim')
        self.extras = Endpoint(self.credentials, 'extras')
        self.ipam = Endpoint(self.credentials, 'ipam')
        self.secrets = Endpoint(self.credentials, 'secrets')
        self.tenancy = Endpoint(self.credentials, 'tenancy')
        self.virtualization = Endpoint(self.credentials, 'virtualization')


class Endpoint(object):
    def __init__(self, credentials, endpoint):
        self.base_url = credentials[0]
        self.endpoint = endpoint
        self.resource = ''
        self.auth = credentials[1]
        self.tls_verify = credentials[2]

    def create(self, _resource, **filters):
        self.resource = _resource
        req = Request(make_url(self.base_url, self.endpoint, self.resource), 
            self.auth, self.tls_verify)
        res = req.post(**filters)
        if res.status == 201:
            return loads(res.read())
        else:
            raise CorsairError(f'Error creating element: {filters}')
    
    def read(self, _resource, **filters):
        'Gets multiple elements filtered by filters - blank to show all'
        self.resource = _resource
        offset = 0 if not 'offset' in filters else filters['offset']
        limit = 1000 if not 'limit' in filters else filters['limit']
        filters.update({'offset':offset,'limit':limit})
        req = Request(make_url(self.base_url, self.endpoint, self.resource), 
            self.auth, self.tls_verify)
        try:
            res = req.get(**filters)
        except timeout:
            raise CorsairError('Operation timedout')
        return loads(res.read())  # test for possible Netbox errors
    
    def update(self, _resource, **filters):
        'Set the properties of a given element'
        self.resource = _resource
        req = Request(make_url(self.base_url, self.endpoint, self.resource), 
            self.auth, self.tls_verify)
        try:
            res = req.patch(**filters)
        except timeout:
            raise CorsairError(f'Operation timedout')
        if res.status == 200:
            return loads(res.read())
        else:
            raise CorsairError(f'Error updating: {self.resource}')
        
    def delete(self, _resource, **filters):
        'Deletes a given element'
        self.resource = _resource
        req = Request(make_url(self.base_url, self.endpoint, self.resource), 
            self.auth, self.tls_verify)
        try:
            res = req.delete(**filters)
        except timeout:
            raise CorsairError(f'Operation timedout')
        if res.status == 204:
            return res.status
        else:
            raise CorsairError(f'Error deleting: {self.resource}')


class Request(object):
    def __init__(self, url, auth, tls_verify):
        self.url = url
        self.timeout = TIMEOUT
        self.context = None if tls_verify else _create_unverified_context()
        self.headers = {
            'Content-Type': 'application/json', 
            'Authorization': f'Token {auth}'
        }
    
    def get(self, **filters):
        url = f'{self.url}?{urlencode(filters)}' if filters else self.url
        req = urllib.request.Request(url, headers=self.headers, method='GET')
        return urllib.request.urlopen(req, timeout=self.timeout, context=self.context)
    
    def patch(self, **filters):
        url = f'{self.url}/'
        req = urllib.request.Request(url, headers=self.headers, 
            data=dumps(filters).encode('utf-8'), method='PATCH')
        return urllib.request.urlopen(req, timeout=self.timeout, context=self.context)
    
    def post(self, **filters):
        url = f'{self.url}/'
        req = urllib.request.Request(url, headers=self.headers,
            data=dumps(filters).encode('utf-8'), method='POST')
        return urllib.request.urlopen(req, timeout=self.timeout, context=self.context)
    
    def delete(self):
        url = f'{self.url}/'
        req = urllib.request.Request(url, headers=self.headers, 
            method='DELETE')
        return urllib.request.urlopen(req, timeout=self.timeout, context=self.context)
