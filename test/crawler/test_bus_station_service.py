import unittest
from os.path import dirname

from crawler.service.bus_station_service import BusStationService


class TestBusRouteService(unittest.TestCase):
	def setUp(self):
		self.bus_station_service = BusStationService()

	def test_request_bus_station_data(self):
		result = self.bus_station_service.request_bus_station_data('团结桥')
		assert result is not None
		assert len(result) > 0

	def test_handle_bus_station_list_data(self):
		with open(dirname(__file__) + '/resource/test_bus_query.html', encoding='utf-8') as file:
			content = file.read()
		result = self.bus_station_service.handle_bus_station_list_data(content, '团结桥')
		assert result is not None
		assert len(result) > 0

	def test_save_bus_station_data_to_db(self):
		with open(dirname(__file__) + '/resource/test_bus_query.html', encoding='utf-8') as file:
			content = file.read()
		result = self.bus_station_service.handle_bus_station_list_data(content, '团结桥')
		for bus_station in result:
			self.bus_station_service.save_bus_station_data_to_db(bus_station)

	def test_crawl_bus_station_data(self):
		self.bus_station_service.crawl_bus_station_data('金鸡湖')


if __name__ == '__main__':
	unittest.main()
