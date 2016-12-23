import threading
import time
from datetime import datetime

import pymongo
from schedule import Scheduler

from common import log
from common import mongodb_service, utils
from crawler.core import config
from crawler.proxy import proxy_strategy

TASK_INTERVAL = 60
FAILED_COUNT_BORDER = 0
SUCCESS_COUNT_BORDER = 50
MIN_PROXY_COUNT = 5

REDIS_KEY_LAST_CHECK_IP_TIME = "last_check_ip_time"


class ProxyPool(object):
	TABLE_NAME = 'proxy_pool'

	def __init__(self):
		self.redis_client = config.redis_client
		self.collection = mongodb_service.get_collection(config.mongodb, self.TABLE_NAME)
		self.collection.create_index([('ip', pymongo.ASCENDING)], unique=True, sparse=True)

	# Singleton
	def __new__(cls, *args, **kwargs):
		if not hasattr(cls, '_instance'):
			org = super(ProxyPool, cls)
			cls._instance = org.__new__(cls, *args)
		return cls._instance

	def random_choice_proxy(self) -> str:
		proxy = self.collection.find().sort(
			[("failed_count", pymongo.ASCENDING), ("validity", pymongo.DESCENDING), ("response_speed", pymongo.ASCENDING),
			 ("update_time", pymongo.DESCENDING)])
		# count = self.collection.count()
		# offset = randrange(1, count)
		# proxy = self.collection.find().skip(offset).limit(1)
		return proxy[0]['ip']

	def add_failed_time(self, ip):
		proxy = self.collection.find_one({'ip': ip})
		if proxy is not None:
			failed_count = proxy['failed_count'] + 1
			log.info("ip: %s 失败次数+1 已失败次数%s次" % (ip, failed_count))
			if failed_count <= FAILED_COUNT_BORDER:
				try:
					self.collection.update_one({'ip': ip}, {"$set": {'update_time': utils.get_utc_time(), 'failed_count': failed_count}})
				except:
					pass
			else:
				try:
					self.collection.delete_one({'ip': ip})
					log.info("ip: %s 失败次数过多已删除" % ip)
				except:
					pass
		self.crawl_proxy_task()

	def add_success_time(self, ip):
		proxy = self.collection.find_one({'ip': ip})
		if proxy is not None:
			success_count = proxy['success_count'] + 1
			log.info("ip: %s 成功次数+1 已成功次数%s次" % (ip, success_count))
			if success_count <= SUCCESS_COUNT_BORDER:
				try:
					self.collection.update_one({'ip': ip}, {"$set": {'update_time': utils.get_utc_time(), 'success_count': success_count}})
				except:
					pass
			else:
				try:
					self.collection.delete_one({'ip': ip})
					log.info("ip: %s 成功次数过多已删除" % ip)
				except:
					pass
		self.crawl_proxy_task()

	def crawl_proxy_task(self, check_num: bool = True):
		if check_num:
			count = self.collection.count()
			if count > MIN_PROXY_COUNT:
				return
		log.info("开始抓取代理")
		proxy_list = proxy_strategy.crawl_proxy()
		log.info("开始保存")
		for proxy in proxy_list:
			if not self.collection.find_one({'ip': proxy.ip}):
				self.collection.insert_one(proxy.__dict__)
				log.info('保存了:' + proxy.ip)
		log.info("保存结束")

	def check_ip_availability_task(self):
		last_check_time = self.redis_client.get(REDIS_KEY_LAST_CHECK_IP_TIME)
		now_time = datetime.utcnow().timestamp()
		if last_check_time is not None and (now_time - float(last_check_time)) < (TASK_INTERVAL * 60):
			return
		self.redis_client.set(REDIS_KEY_LAST_CHECK_IP_TIME, now_time)

		proxy_list = self.collection.find()
		for proxy in proxy_list:
			ip = proxy['ip']
			start_time = time.time()
			response = utils.http_get('http://lwons.com/wx', timeout=10)
			is_success = response.status_code == 200
			response.close()
			if not is_success:
				try:
					self.collection.delete_one({'ip': ip})
				except:
					pass
				log.info('Check ip %s FAILED' % ip)
			else:
				elapsed = round(time.time() - start_time, 4)
				try:
					self.collection.update_one({'ip': ip}, {"$set": {'update_time': utils.get_utc_time(), 'response_speed': elapsed, 'validity': True}})
				except:
					pass
				log.info('Check ip %s SUCCESS' % ip)

	def start(self):
		self.crawl_proxy_task(False)

		def task():
			self.check_ip_availability_task()
			schedule = Scheduler()
			schedule.every(10).minutes.do(self.check_ip_availability_task)

			while True:
				schedule.run_pending()
				time.sleep(1)

		thread = threading.Thread(target=task)
		thread.start()

	def drop_proxy(self):
		self.collection.delete_many({})


proxy_pool = ProxyPool()
