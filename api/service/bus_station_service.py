import requests
from lxml import etree
from lxml.etree import XMLSyntaxError
from lxml.etree import XPathEvalError

from api import config
from api.model.bus_station import BusStation
from api.model.real_time_bus import RealTimeBus
from common import mongodb_service, log


class BusStationService(object):
	TABLE_BUS_STATION = 'bus_station'

	def __init__(self):
		self.bus_station_collection = mongodb_service.get_collection(config.mongodb, self.TABLE_BUS_STATION)

	def query_bus_station_by_name(self, station_name):
		station_list = []
		station_cursor = self.bus_station_collection.find({'name': station_name})
		for station_dict in station_cursor:
			station = BusStation.create(station_dict)
			station_list.append(station)
		return station_list

	def fuzzy_query_bus_station_by_name(self, station_name, **kwargs):
		try:
			page = kwargs['page']
		except KeyError:
			page = None
		try:
			offset = kwargs['offset']
		except KeyError:
			offset = None

		station_list = []
		if (isinstance(page, int) and page >= 0) and (isinstance(offset, int) and offset > 0):
			station_cursor = self.bus_station_collection.find({'name': {'$regex': station_name}}).skip(page).limit(offset)
		else:
			station_cursor = self.bus_station_collection.find({'name': {'$regex': station_name}})
		for station_dict in station_cursor:
			station = BusStation.create(station_dict)
			station_list.append(station)
		return station_list

	def get_real_time_station_data(self, number):
		html = self.request_real_time_station_data(number)
		real_time_bus_list = self.handle_real_time_station_data(html)
		return real_time_bus_list

	def request_real_time_station_data(self, number):
		url = 'http://www.szjt.gov.cn/apts/default.aspx'
		data = {
			'ctl00$MainContent$StandName': '',
			'ctl00$MainContent$Watch': '查看',
			'ctl00$MainContent$StandCode': number,
			'__VIEWSTATE': '/wEPDwULLTE5ODM5MjcxNzlkZG5FgcZjEw/Xcik6rLaQKQqjiJG1N/LcEaJpbqk1zMfT',
			'__VIEWSTATEGENERATOR': '7BCA6D38',
			'__EVENTVALIDATION': '/wEWBQKV37ujDALq+uyKCAKkmJj/DwL0+sTIDgLl5vKEDjV831PkO9I9rzINcIDwIwK31J8x9g8zuNZKL7+XkZX5'
		}
		headers = {
			'Referer': 'http://www.szjt.gov.cn/apts/default.aspx',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'Content-Type': 'application/x-www-form-urlencoded',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
		}
		try:
			response = requests.post(url, data=data, headers=headers, timeout=20)
		except Exception as e:
			log.error(e)
			return None
		if response is None:
			return None
		return response.text

	def handle_real_time_station_data(self, content) -> []:
		try:
			html = etree.HTML(content)
		except XMLSyntaxError as e:
			log.error(e)
			return []
		except ValueError as e:
			log.error(e)
			return []
		try:
			content_list = html.xpath("//span[@id='MainContent_DATA']//table//tr")
		except XPathEvalError as e:
			log.error(e)
			return []

		real_time_bus_list = []
		for index, content_item in enumerate(content_list):
			if index == 0:
				continue

			route = content_item.getchildren()[0].xpath('a')[0].text
			direction = content_item.getchildren()[1].text
			license = content_item.getchildren()[2].text
			update_time = content_item.getchildren()[3].text
			station_spacing = content_item.getchildren()[4].text

			real_time_bus = RealTimeBus()
			real_time_bus.route = route
			real_time_bus.direction = direction
			real_time_bus.license = license
			real_time_bus.update_time = update_time
			real_time_bus.station_spacing = station_spacing
			real_time_bus_list.append(real_time_bus)
		return real_time_bus_list
