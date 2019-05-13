from base64 import b64encode
from ssl import _create_unverified_context
from urllib.parse import urlsplit


TIMEOUT = 20  # default timeout in seconds


class CorsairError(Exception):
    pass


def gen_auth(username, password):
    'Generate basic authorization using username and password'
    return b64encode(f'{username}:{password}'.encode('utf-8')).decode()

def make_url(base_url, endpoint, resource):
    'Corsair creates URLs using this method'
    base_url = urlsplit(base_url)
    path = base_url.path + f'/{endpoint}/{resource}'
    path = path.replace('//', '/')
    path = path[:-1] if path.endswith('/') else path
    return base_url._replace(path=path).geturl()
