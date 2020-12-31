import requests

from http import HTTPStatus
from pprint import pprint
from urllib.parse import urljoin

from django.conf import settings

if getattr(settings, 'DISABLE_URLLIB3_WARNINGS', False):
    import urllib3
    urllib3.disable_warnings()


class BearerAuth(requests.auth.AuthBase):

    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


class HTTPAPIClient(object):
    base_url = None

    def __init__(self, base_url):
        self.base_url = base_url

    def build_url(self, path):
        # return urljoin(self.base_url, path)
        url = ''.join([self.base_url, path])  # quick fix for base urls with relative paths
        return url

    def get_auth(self):
        return None

    def get_default_headers(self):
        return None

    def post(self, path, data=None, json=None,  headers=None, **kwargs):
        r = requests.post(
            self.build_url(path),
            json=json,
            data=data,
            headers={
                **(self.get_default_headers() or {}),
                **(headers or {})
            } or None,
            auth=self.get_auth(),
            **kwargs
        )
        return r

    def get(self, path, data=None, headers=None, **kwargs):
        r = requests.get(
            self.build_url(path),
            data=data,
            headers={
                **(self.get_default_headers() or {}),
                **(headers or {})
            } or None,
            auth=self.get_auth(),
            **kwargs
        )
        return r
