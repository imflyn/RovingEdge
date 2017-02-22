import unittest

from api.service.bus_station_service import BusStationService


class TestBusStationService(unittest.TestCase):
	def setUp(self):
		self.bus_station_service = BusStationService()
		pass

	def test_paging_fuzzy_query_bus_route_by_name(self):
		station_list = self.bus_station_service.fuzzy_query_bus_station_by_name('二')
		assert len(station_list) > 0
		station_list = self.bus_station_service.fuzzy_query_bus_station_by_name('二', page=1, offset=2)
		assert len(station_list) > 0


if __name__ == '__main__':
	unittest.main()
