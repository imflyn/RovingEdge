import unittest
from os.path import dirname

from crawler.service.bus_route_service import BusRouteService


class TestBusRouteService(unittest.TestCase):
	def setUp(self):
		self.bus_route_service = BusRouteService()
		pass

	def test_request_bus_route_data(self):
		result = self.bus_route_service.request_bus_route_data()
		assert result is not None
		assert len(result) > 0

	def test_handle_bus_route_data(self):
		with open(dirname(__file__) + '/resource/test_bus_route_service.xml', encoding='utf-8') as file:
			content = file.read()
		result = self.bus_route_service.handle_bus_route_data(content)
		assert result is not None
		assert len(result) > 0


if __name__ == '__main__':
	unittest.main()
