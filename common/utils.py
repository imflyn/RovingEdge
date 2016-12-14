import uuid

import requests
from requests import Response
from requests.adapters import HTTPAdapter


def http_request(url: str, timeout=30) -> Response:
    session = requests.Session()
    session.mount('https://', HTTPAdapter(max_retries=5))
    session.mount('http://', HTTPAdapter(max_retries=5))
    response = session.get(url, timeout=timeout)
    response.encoding = 'utf-8'
    return response


def get_uuid():
    return str(uuid.uuid1())
