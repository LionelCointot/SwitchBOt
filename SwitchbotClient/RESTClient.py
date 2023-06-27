import base64
import hashlib
import hmac
import time
from typing import Any
import requests
import humps



class RESTClient:

    def __init__(self, base_uri: str):
        self.session = requests.Session()
        self.base_uri = base_uri

        self.session.headers['Content-Type']='application/json'
        self.session.headers['charset']='utf8'

    def add_header(self, key:str, value: str):
        self.session.headers[key] = value
    
    def remove_header(self, key:str):
        self.session.headers.pop(key, None)

    def request(self, method: str, path: str, **kwargs) -> Any:
        url = f"{self.base_uri}/{path}"
        response = requests.Response()
        try:
            response = self.session.request(method, url, **kwargs)

        #TODO: à Tracer
        except Exception:
            pass
            
        if response.status_code != 200:
            raise RuntimeError(
                f"Server returns status {response.status_code}"
            )

        response_in_json = response.json()
        if response_in_json["statusCode"] != 100:
            raise RuntimeError(f'An error occurred: {response_in_json["message"]}')

        return response_in_json

    def get(self, path: str, **kwargs) -> Any:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs) -> Any:
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs) -> Any:
        return self.request("PUT", path, **kwargs)

    def delete(self, path: str, **kwargs) -> Any:
        return self.request("DELETE", path, **kwargs)
