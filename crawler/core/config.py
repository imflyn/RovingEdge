import logging

from requests.packages.urllib3.connectionpool import log as requests_log
from selenium.webdriver.remote.remote_connection import LOGGER as selenium_log

from common import mongodb_service

selenium_log.setLevel(logging.WARNING)
requests_log.setLevel(logging.WARNING)

DATABASE_NAME = "Suzhou_Bus"

# HOST
HOST = 'localhost'
PORT = 27017

# MongoDB
mongodb = mongodb_service.get_db(mongodb_service.get_client(HOST, PORT), DATABASE_NAME)

# phantomjs_path = 'D:\Development\python3\Scripts\phantomjs.exe'
phantomjs_path = 'C:\Flyn\Development\SDK\python3\Scripts\phantomjs.exe'
