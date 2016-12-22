import collections

import requests
from lxml import etree
from lxml.etree import XMLSyntaxError
from lxml.etree import XPathEvalError
from requests.adapters import HTTPAdapter

from common import log, mongodb_service, utils
from crawler.core import config
from crawler.model.bus_station import BusStation
from crawler.proxy.proxy_pool import proxy_pool


class BusStationService(object):
	TABLE_NAME = 'bus_station'

	def __init__(self):
		self.collection = mongodb_service.get_collection(config.mongodb, self.TABLE_NAME)

	def handle_bus_station_list_data(self, content, station_name) -> []:
		log.info('爬取公交站台-->处理<{station_name}>站台信息开始'.format(station_name=station_name))
		try:
			html = etree.HTML(content)
		except XMLSyntaxError:
			log.info('爬取公交站台-->处理<{station_name}>站台信息失败'.format(station_name=station_name))
			return []
		except ValueError:
			log.info('爬取公交站台-->处理<{station_name}>站台信息失败'.format(station_name=station_name))
			return []
		try:
			content_list = html.xpath("//span[@id='MainContent_DATA']//table//tr")
		except XPathEvalError:
			log.info('爬取公交站台-->处理<{station_name}>站台信息失败'.format(station_name=station_name))
			return []

		station_list = []
		for index, content_item in enumerate(content_list):
			if index == 0:
				continue

			name = content_item.getchildren()[0].xpath('a')[0].text
			number = content_item.getchildren()[1].text
			area = content_item.getchildren()[2].text
			road = content_item.getchildren()[3].text
			road_segment = content_item.getchildren()[4].text
			road_direction = content_item.getchildren()[5].text

			bus_station = BusStation()
			bus_station.id = utils.get_uuid()
			bus_station.name = name
			bus_station.number = number
			bus_station.area = area
			bus_station.road = road
			bus_station.road_segment = road_segment
			bus_station.road_direction = road_direction
			station_list.append(bus_station)
		log.info('爬取公交站台-->处理<{station_name}>站台信息成功，获得<{station_count}>个站台信息'.format(station_name=station_name, station_count=len(station_list)))
		return station_list

	def request_bus_station_data(self, station_name):
		# http://www.szjt.gov.cn/BusQuery/default.aspx?cid=175ecd8d-c39d-4116-83ff-109b946d7cb4
		# ctl00$MainContent$StandName 团结桥
		# ctl00$MainContent$SearchCode 搜索
		# __VIEWSTATE /wEPDwULLTE5ODM5MjcxNzlkZAmiJJ2tnI/uORAHha02uiTP20zkcIPFI/03+QRVt2jm
		# __VIEWSTATEGENERATOR 1DDAEB65
		# __EVENTVALIDATION /wEWBQLCvY65BALq+uyKCAKkmJj/DwL0+sTIDgLl5vKEDsL/hpJTaG5nWiRLbcu6Hd+JXovreFUihHtwVJ7zNsPc
		url = 'http://www.szjt.gov.cn/BusQuery/default.aspx?cid=175ecd8d-c39d-4116-83ff-109b946d7cb4'
		data = {
			'ctl00$MainContent$StandName': station_name,
			'ctl00$MainContent$SearchCode': '搜索',
			'__VIEWSTATE': '/wEPDwULLTE5ODM5MjcxNzlkZAmiJJ2tnI/uORAHha02uiTP20zkcIPFI/03+QRVt2jm',
			'__VIEWSTATEGENERATOR': '1DDAEB65',
			'__EVENTVALIDATION': '/wEWBQLCvY65BALq+uyKCAKkmJj/DwL0+sTIDgLl5vKEDsL/hpJTaG5nWiRLbcu6Hd+JXovreFUihHtwVJ7zNsPc'
		}
		headers = {
			'Referer': 'http://www.szjt.gov.cn/BusQuery/default.aspx?cid=175ecd8d-c39d-4116-83ff-109b946d7cb4',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'Content-Type': 'application/x-www-form-urlencoded',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
		}
		session = requests.Session()
		session.mount('https://', HTTPAdapter(max_retries=2))
		session.mount('http://', HTTPAdapter(max_retries=2))
		if config.USE_PROXY:
			retry_time = 1
			while True:
				ip = proxy_pool.random_choice_proxy()
				proxies = {
					"http": ip
				}
				log.info('爬取公交站台-->处理<{station_name}>站台，第<{retry_time}>次尝试,使用代理<{ip}>发送Http请求'.format(station_name=station_name, ip=ip, retry_time=retry_time))
				try:
					response = session.post(url, data=data, headers=headers, timeout=20, proxies=proxies)
					proxy_pool.add_success_time(ip)
					break
				except Exception as e:
					log.info('爬取公交站台-->处理<{station_name}>站台，第<{retry_time}>次尝试,使用代理<{ip}>发送Http请求失败'
					         .format(station_name=station_name, ip=ip, retry_time=retry_time))
					retry_time += 1
					log.error(e)
					proxy_pool.add_failed_time(ip)
		else:
			try:
				response = session.post(url, data=data, headers=headers, timeout=20)
			except Exception as e:
				log.error(e)
				return None
		if response is None:
			return None
		response.encoding = 'utf-8'
		return response.text

	# def request_bus_station_data(self, station_name):
	#     driver = webdriver.PhantomJS(executable_path=config.phantomjs_path, service_args=['--load-images=no'])
	#     # driver = webdriver.Chrome()
	#     driver.set_page_load_timeout(40)
	#     log.info('爬取公交站台-->获取<{station_name}>站台信息开始'.format(station_name=station_name))
	#     try:
	#         driver.get("http://www.szjt.gov.cn/BusQuery/default.aspx?cid=175ecd8d-c39d-4116-83ff-109b946d7cb4")
	#     except TimeoutException as e:
	#         log.warn(e)
	#         return None
	#     driver.find_element_by_id("MainContent_StandName").send_keys(station_name)
	#     driver.find_element_by_id("MainContent_SearchCode").click()
	#     time.sleep(0.5)
	#     body = driver.page_source
	#     log.info('爬取公交站台-->获取<{station_name}>站台信息成功'.format(station_name=station_name))
	#     return body

	def save_bus_station_data_to_db(self, bus_station: BusStation):
		try:
			if not self.collection.find_one({'number': bus_station.number}):
				self.collection.insert_one(bus_station.__dict__)
			else:
				self.collection.replace_one({'number': bus_station.number}, bus_station.__dict__)
		except Exception as e:
			log.error(e)

	def crawl_bus_station_data(self, station_name):
		bus_station_html = self.request_bus_station_data(station_name)
		bus_station_list = self.handle_bus_station_list_data(bus_station_html, station_name)
		if isinstance(bus_station_list, collections.Iterable) and len(bus_station_list) > 0:
			log.info('爬取公交站台-->保存<{station_name}>站台信息开始'.format(station_name=station_name))
			for bus_station in bus_station_list:
				self.save_bus_station_data_to_db(bus_station)
			log.info('爬取公交站台-->保存<{station_name}>站台信息成功'.format(station_name=station_name))
		else:
			log.info('爬取公交站台-->站台名<{station_name}>没有获取到站台信息'.format(station_name=station_name))
