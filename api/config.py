import logging

import redis
from requests.packages.urllib3.connectionpool import log as requests_log
from selenium.webdriver.remote.remote_connection import LOGGER as selenium_log

from common import mongodb_service

selenium_log.setLevel(logging.WARNING)
requests_log.setLevel(logging.ERROR)

DATABASE_NAME = "Suzhou_Bus"

# HOST
HOST = 'localhost'
PORT = 27017

# MongoDB
mongodb = mongodb_service.get_db(mongodb_service.get_client(HOST, PORT), DATABASE_NAME)

REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DATABASE_NAME = 0

# Redis
redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DATABASE_NAME)
