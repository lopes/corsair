import urllib.request

from urllib.parse import urlencode
from json import loads
from socket import timeout

from corsair import CorsairError


class Api(object):
    def __init__(self, base_url, auth):
        self.base_url = base_url
        self.auth = auth
        self.credentials = (self.base_url, self.auth)

        self.file = Endpoint(self.credentials, 'file')
        self.url = Endpoint(self.credentials, 'url')
        self.domain = Endpoint(self.credentials, 'domain')
        self.ip_address = Endpoint(self.credentials, 'ip-address')
        self.comments = Endpoint(self.credentials, 'comments')


class Endpoint(object):
    def __init__(self, credentials, endpoint):
        self.base_url = credentials[0]
        self.endpoint = endpoint
        self.resource = ''
        self.auth = credentials[1]
    
    def create(self, _resource, **filters):
        self.resource = _resource  # resource is a VT keyword
        req = Request(self.make_url(), self.auth)
        res = req.post(**filters)
        if res.status == 201:
            return loads(res.read())
        else:
            raise CorsairError(f'Error creating element: {filters}')
    
    def read(self, _resource, **filters):
        self.resource = _resource  # resource is a VT keyword
        req = Request(self.make_url(), self.auth)

        try:
            res = req.get(**filters)
        except timeout:
            raise CorsairError('Operation timedout')

        if 'output_file' in filters:  # user requested to download a file
            with open(filters['output_file'], 'wb') as f:
                f.write(res.read())
            return res.status

        if res.status == 200:  #TODO better error checking
            return loads(res.read())
        else:
            raise CorsairError('Not found')
    
    def make_url(self):
        url = f'{self.base_url}/{self.endpoint}/{self.resource}'
        url.replace('//', '/')
        url = url[:-1] if url.endswith('/') else url
        return url


class Request(object):
    def __init__(self, url, auth):
        self.url = url
        self.auth = auth
        self.timeout = 20  # seconds
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    
    def get(self, **filters):
        if 'apikey' not in filters:
            filters.update({'apikey': self.auth})
        url = f'{self.url}?{urlencode(filters)}' if filters else self.url
        req = urllib.request.Request(url, headers=self.headers, method='GET')
        return urllib.request.urlopen(req, timeout=self.timeout)
    
    def post(self, **filters):
        if 'apikey' not in filters:
            filters.update({'apikey': self.auth})
        if 'file' in filters:
            self.headers['Content-Type'] = 'application/x-www-form-urlencoded'
        req = urllib.request.Request(self.url, headers=self.headers, 
            data=urlencode(filters).encode('utf-8'), method='POST')
        return urllib.request.urlopen(req, timeout=self.timeout)
