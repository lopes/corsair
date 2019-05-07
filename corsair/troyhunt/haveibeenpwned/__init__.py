import urllib.request

from urllib.parse import urlencode
from json import loads
from socket import timeout

from corsair import CorsairError


class Api(object):
    def __init__(self, base_url):
        self.base_url = base_url if base_url[-1] != '/' else base_url[:-1]
        self.credentials = (self.base_url,)

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
    
    def read(self, resource, **filters):
        self.resource = resource
        req = Request(self.make_url())

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
    
    def make_url(self):
        url = f'{self.base_url}/{self.endpoint}/{self.resource}'
        url.replace('//', '/')
        url = url[:-1] if url.endswith('/') else url
        return url


class Request(object):
    def __init__(self, url):
        self.url = url
        self.timeout = 20  # seconds
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'User-Agent': 'python-urllib',
            'api-version': '2'
        }
    
    def get(self, **filters):
        url = f'{self.url}?{urlencode(filters)}' if filters else self.url
        req = urllib.request.Request(url, headers=self.headers, method='GET')
        return urllib.request.urlopen(req, timeout=self.timeout)
