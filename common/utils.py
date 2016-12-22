import datetime
import uuid

import requests
from requests import Response
from requests.adapters import HTTPAdapter


def http_get(url: str, headers=None, timeout=30) -> Response:
	session = requests.Session()
	session.mount('https://', HTTPAdapter(max_retries=5))
	session.mount('http://', HTTPAdapter(max_retries=5))
	response = session.get(url, headers=headers, timeout=timeout)
	response.encoding = 'utf-8'
	return response


def http_post(url: str, data: {}, headers=None, proxies=None, timeout=30) -> Response:
	session = requests.Session()
	session.mount('https://', HTTPAdapter(max_retries=5))
	session.mount('http://', HTTPAdapter(max_retries=5))
	response = session.post(url, data=data, headers=headers, timeout=timeout, proxies=proxies)
	response.encoding = 'utf-8'
	return response


def get_uuid():
	return str(uuid.uuid1())


def get_utc_time() -> str:
	return datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
