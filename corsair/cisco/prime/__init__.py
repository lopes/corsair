import urllib.request

from urllib.parse import urlencode
from json import loads
from socket import timeout

from corsair import CorsairError, gen_auth


class Api(object):
    def __init__(self, base_url, username, password):
        self.base_url = base_url if base_url[-1] != '/' else base_url[:-1]
        self.auth = gen_auth(username, password)
        self.credentials = (self.base_url, self.auth)

        self.data = Endpoint(self.credentials, 'data')
        self.op = Endpoint(self.credentials, 'op')


class Endpoint(object):
    def __init__(self, credentials, endpoint):
        self.base_url = credentials[0]
        self.endpoint = endpoint
        self.resource = ''
        self.auth = credentials[1]
    
    def read(self, _resource, **filters):
        self.resource = f'{_resource}.json'  # will only deal with JSON outputs
        first_result = 0 if 'firstResult' not in filters else filters['firstResult']
        max_results = 1000 if 'maxResults' not in filters else filters['maxResults']
        filters.update({'firstResult':first_result, 'maxResults':max_results})
        req = Request(self.make_url(), self.auth)
        try:
            res = req.get(**filters)
        except timeout:
            raise CorsairError('Operation timedout')
        return loads(res.read())  # test for possible Prime errors
    
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
            'Content-Type': 'application/json',
            'Authorization': f'Basic {self.auth}'
        }

    def get(self, **filters):
        url = f'{self.url}?{self.dotted_filters(**filters)}' if filters else self.url
        req = urllib.request.Request(url, headers=self.headers, method='GET')
        return urllib.request.urlopen(req) 
    
    def dotted_filters(self, **filters):
        'Prime filters start with a dot'
        if not filters:
            return ''
        else:
            return f'.{urlencode(filters).replace("&", "&.")}'
