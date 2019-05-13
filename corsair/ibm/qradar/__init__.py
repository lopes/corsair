import urllib.request

from urllib.parse import urlencode
from json import loads
from socket import timeout
from ssl import _create_unverified_context

from corsair import *


class Api(object):
    def __init__(self, base_url, auth, tls_verify=True):
        self.base_url = base_url if base_url[-1] != '/' else base_url[:-1]
        self.auth = auth
        self.tls_verify = tls_verify
        self.credentials = (self.base_url, self.auth, self.tls_verify)

        self.analytics = Endpoint(self.credentials, 'analytics')
        self.ariel = Endpoint(self.credentials, 'ariel')
        self.asset_model = Endpoint(self.credentials, 'asset_model')
        self.auth = Endpoint(self.credentials, 'auth')
        self.config = Endpoint(self.credentials, 'config')
        self.data_classification = Endpoint(self.credentials, 'data_classification')
        self.forensics = Endpoint(self.credentials, 'forensics')
        self.gui_app_framework = Endpoint(self.credentials, 'gui_app_framework')
        self.help = Endpoint(self.credentials, 'help')
        self.qrm = Endpoint(self.credentials, 'qrm')
        self.reference_data = Endpoint(self.credentials, 'reference_data')
        self.scanner = Endpoint(self.credentials, 'scanner')
        self.services = Endpoint(self.credentials, 'services')
        self.siem = Endpoint(self.credentials, 'siem')
        self.staged_config = Endpoint(self.credentials, 'staged_config')
        self.system = Endpoint(self.credentials, 'system')


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
            raise CorsairError('Could not create requisition')
        
    def read(self, _resource, **filters):
        self.resource = _resource
        req = Request(make_url(self.base_url, self.endpoint, self.resource), 
            self.auth, self.tls_verify)
        try:
            res = req.get(**filters)
        except timeout:
            raise CorsairError('Operation timedout')
        if res.status == 200:
            crange = res.headers['Content-Range'].split(' ')[1] \
                if 'Content-Range' in res.headers else None
            return {'results': loads(res.read()), 'range': crange}
        else:
            raise CorsairError('Not found')


class Request(object):
    def __init__(self, url, auth, tls_verify):
        self.url = url
        self.timeout = TIMEOUT
        self.context = None if tls_verify else _create_unverified_context()
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Version': '8.0',
            'SEC': auth
        }
    
    def get(self, **filters):
        if 'Range' in filters:
            self.headers.update({'Range': filters['Range']})
            filters.pop('Range')
        url = f'{self.url}?{urlencode(filters)}' if filters else self.url
        req = urllib.request.Request(url, headers=self.headers, method='GET')
        return urllib.request.urlopen(req, timeout=self.timeout, context=self.context)
    
    def post(self, **filters):
        url = f'{self.url}?{urlencode(filters)}' if filters else self.url
        req = urllib.request.Request(url, headers=self.headers, method='POST')
        return urllib.request.urlopen(req, timeout=self.timeout, context=self.context)
