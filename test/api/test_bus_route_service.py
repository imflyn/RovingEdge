import unittest

from api.service.bus_route_service import BusRouteService


class TestBusRouteService(unittest.TestCase):
    def setUp(self):
        self.bus_route_service = BusRouteService()

    def test_query_bus_route_by_name(self):
        route_list = self.bus_route_service.query_bus_route_by_name('1')
        assert len(route_list) > 0


if __name__ == '__main__':
    unittest.main()
