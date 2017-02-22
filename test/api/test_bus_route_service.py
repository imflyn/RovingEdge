import unittest

from api.service.bus_route_service import BusRouteService


class TestBusRouteService(unittest.TestCase):
	def setUp(self):
		self.bus_route_service = BusRouteService()

	def test_query_bus_route_by_name(self):
		route_list = self.bus_route_service.query_bus_route_by_name('1')
		assert len(route_list) > 0

	def test_fuzzy_query_bus_route_by_name(self):
		route_list = self.bus_route_service.fuzzy_query_bus_route_by_name('2')
		assert len(route_list) > 0

	def test_paging_fuzzy_query_bus_route_by_name(self):
		route_list = self.bus_route_service.fuzzy_query_bus_route_by_name('2')
		assert len(route_list) > 0
		route_list = self.bus_route_service.fuzzy_query_bus_route_by_name('2', page=1, offset=2)
		assert len(route_list) > 0


if __name__ == '__main__':
	unittest.main()
