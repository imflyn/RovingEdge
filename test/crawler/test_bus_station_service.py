import unittest
from os.path import dirname

from twisted.internet import reactor
from twisted.internet.defer import Deferred

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

	def test_crawl_bus_station_data_concurrent(self):
		bus_station_list = ['团结桥', '南门', '人民桥', '观前街', '苏州乐园', '金鸡湖', '独墅湖', '苏苑', '水香', '友联',
		                    '团结桥', '南门', '人民桥', '观前街', '苏州乐园', '金鸡湖', '独墅湖', '苏苑', '水香', '友联',
		                    '团结桥', '南门', '人民桥', '观前街', '苏州乐园', '金鸡湖', '独墅湖', '苏苑', '水香', '友联',
		                    '团结桥', '南门', '人民桥', '观前街', '苏州乐园', '金鸡湖', '独墅湖', '苏苑', '水香', '友联',
		                    '团结桥', '南门', '人民桥', '观前街', '苏州乐园', '金鸡湖', '独墅湖', '苏苑', '水香', '友联']

		def crawl_bus_station(bus_station) -> Deferred:
			defer = Deferred()
			self.bus_station_service.crawl_bus_station_data(bus_station)
			return defer

		def task():
			def callbacks_finished(_):
				callbacks_finished.count += 1
				if callbacks_finished.count == len(bus_station_list):
					reactor.stop()

			callbacks_finished.count = 0

			for bus_station_entry in bus_station_list:
				defer = crawl_bus_station(bus_station_entry)
				defer.addBoth(callbacks_finished)
				defer.callback('')

		reactor.callWhenRunning(task)
		reactor.run()


if __name__ == '__main__':
	unittest.main()
