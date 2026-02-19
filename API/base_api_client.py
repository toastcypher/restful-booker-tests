import requests

class BaseApiClient:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/")
        self._token = None

    def set_token(self, token):
        self._token = token

    def request(self, method, path, params=None, json=None, headers=None):
        url = f"{self.base_url}{path}"

        merged_headers = {}
        if self._token:
            merged_headers["Cookie"] = f"token={self._token}"
        if headers:
            merged_headers.update(headers)

        return requests.request(method, url, params=params, json=json, headers=merged_headers)