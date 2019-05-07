import urllib.request
import re

from urllib.parse import urlencode
from json import loads
from socket import timeout
from ssl import _create_unverified_context

from corsair import *


class Api(object):
    def __init__(self, base_url, username, password, tls_verify=True):
        self.base_url = base_url if base_url[-1] != '/' else base_url[:-1]
        self.auth = gen_auth(username, password)
        self.tls_verify = tls_verify
        self.credentials = (self.base_url, self.auth, self.tls_verify)

        self.ancendpoint = Endpoint(self.credentials, 'ancendpoint')
        self.ancpolicy = Endpoint(self.credentials, 'ancpolicy')
        self.activedirectory = Endpoint(self.credentials, 'activedirectory')
        self.portalglobalsetting = Endpoint(self.credentials, 'portalglobalsetting')
        self.byodportal = Endpoint(self.credentials, 'byodportal')
        self.certificatetemplate = Endpoint(self.credentials, 'certificatetemplate')
        self.threat = Endpoint(self.credentials, 'threat')
        self.egressmatrixcell = Endpoint(self.credentials, 'egressmatrixcell')
        self.endpoint = Endpoint(self.credentials, 'endpoint')
        self.endpointcert = Endpoint(self.credentials, 'endpointcert')
        self.endpointgroup = Endpoint(self.credentials, 'endpointgroup')
        self.guestlocation = Endpoint(self.credentials, 'guestlocation')
        self.guestsmtpnotificationsettings = Endpoint(self.credentials, 'guestsmtpnotificationsettings')
        self.guestssid = Endpoint(self.credentials, 'guestssid')
        self.guesttype = Endpoint(self.credentials, 'guesttype')
        self.guestuser = Endpoint(self.credentials, 'guestuser')
        self.hotspotportal = Endpoint(self.credentials, 'hotspotportal')
        self.sgmapping = Endpoint(self.credentials, 'sgmapping')
        self.sgmappinggroup = Endpoint(self.credentials, 'sgmappinggroup')
        self.service = Endpoint(self.credentials, 'service')
        self.identitygroup = Endpoint(self.credentials, 'identitygroup')
        self.idstoresequence = Endpoint(self.credentials, 'idstoresequence')
        self.internaluser = Endpoint(self.credentials, 'internaluser')
        self.mydeviceportal = Endpoint(self.credentials, 'mydeviceportal')
        self.nspprofile = Endpoint(self.credentials, 'nspprofile')
        self.networkdevice = Endpoint(self.credentials, 'networkdevice')
        self.networkdevicegroup = Endpoint(self.credentials, 'networkdevicegroup')
        self.name = Endpoint(self.credentials, 'name')
        self.sessionservicenode = Endpoint(self.credentials, 'sessionservicenode')
        self.portal = Endpoint(self.credentials, 'portal')
        self.portaltheme = Endpoint(self.credentials, 'portaltheme')
        self.profilerprofile = Endpoint(self.credentials, 'profilerprofile')
        self.smsprovider = Endpoint(self.credentials, 'smsprovider')
        self.sxpconnections = Endpoint(self.credentials, 'sxpconnections')
        self.sxplocalbindings = Endpoint(self.credentials, 'sxplocalbindings')
        self.sxpvpns = Endpoint(self.credentials, 'sxpvpns')
        self.sgt = Endpoint(self.credentials, 'sgt')
        self.sgacl = Endpoint(self.credentials, 'sgacl')
        self.selfregportal = Endpoint(self.credentials, 'selfregportal')
        self.sponsorgroup = Endpoint(self.credentials, 'sponsorgroup')
        self.sponsorgroupmember = Endpoint(self.credentials, 'sponsorgroupmember')
        self.sponsorportal = Endpoint(self.credentials, 'sponsorportal')
        self.sponsoredguestportal = Endpoint(self.credentials, 'sponsoredguestportal')


class Endpoint(object):
    def __init__(self, credentials, endpoint):
        self.base_url = credentials[0]
        self.endpoint = endpoint
        self.resource = ''
        self.auth = credentials[1]
        self.tls_verify = credentials[2]
    
    def read(self, _resource, **filters):
        self.resource = _resource
        page = 1 if not 'page' in filters else filters['page']
        size = 100 if not 'size' in filters else filters['size']
        filters.update({'page':page, 'size':size})
        req = Request(make_url(self.base_url, self.endpoint, self.resource), 
            self.auth, self.tls_verify)
        try:
            res = req.get(**filters)
        except timeout:
            raise CorsairError('Operation timedout')
        return loads(res.read())  # test for possible ISE errors


class Request(object):
    def __init__(self, url, auth, tls_verify):
        self.url = url
        self.auth = auth
        self.timeout = TIMEOUT
        self.context = None if tls_verify else _create_unverified_context()
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Basic {self.auth}'
        }
    
    def get(self, **filters):
        url = f'{self.url}?{self.process_filters(urlencode(filters))}' if filters else self.url
        req = urllib.request.Request(url, headers=self.headers, method='GET')
        return urllib.request.urlopen(req, timeout=self.timeout, context=self.context)
    
    def process_filters(self, filters):
        '''ISE accepts multiple filters with same name, but Python don't.'''
        return re.sub(r'(^|&)(filter)[0-9]+', r'\1\2', filters)
