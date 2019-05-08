import urllib.request

from urllib.parse import urlencode
from json import loads
from socket import timeout
from ssl import _create_unverified_context

from corsair import *


class Api(object):
    def __init__(self, base_url, tls_verify=True):
        self.base_url = base_url if base_url[-1] != '/' else base_url[:-1]
        self.credentials = (self.base_url,)
        self.tls_verify = tls_verify
        self.credentials = (self.base_url, self.tls_verify)

        self.breachedaccount = Endpoint(self.credentials, 'breachedaccount')
        self.breaches = Endpoint(self.credentials, 'breaches')
        self.breach = Endpoint(self.credentials, 'breach')
        self.dataclasses = Endpoint(self.credentials, 'dataclasses')
        self.pasteaccount = Endpoint(self.credentials, 'pasteaccount')
    

class Endpoint(object):
    def __init__(self, credentials, endpoint):
        self.base_url = credentials[0]
        self.endpoint = endpoint
        self.resource = ''
        self.tls_verify = credentials[1]
    
    def read(self, resource, **filters):
        self.resource = resource
        req = Request(make_url(self.base_url, self.endpoint, self.resource), 
            self.tls_verify)

        try:
            res = req.get(**filters)
        except timeout:
            raise CorsairError('Operation timedout')
        except urllib.error.HTTPError:
            raise CorsairError('Not found')

        if res.status == 200:
            return loads(res.read())
        else:
            raise CorsairError('Could not retrieve data')


class Request(object):
    def __init__(self, url, tls_verify):
        self.url = url
        self.timeout = TIMEOUT
        self.context = None if tls_verify else _create_unverified_context()
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'User-Agent': 'python-urllib',
            'api-version': '2'
        }
    
    def get(self, **filters):
        url = f'{self.url}?{urlencode(filters)}' if filters else self.url
        req = urllib.request.Request(url, headers=self.headers, method='GET')
        return urllib.request.urlopen(req, timeout=self.timeout, context=self.context)
