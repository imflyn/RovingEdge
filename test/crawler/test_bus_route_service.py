import unittest
from os.path import dirname

from common import mongodb_service
from crawler.core import config
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

    def test_save_bus_route_data_to_db(self):
        with open(dirname(__file__) + '/resource/test_bus_route_service.xml', encoding='utf-8') as file:
            content = file.read()
        result = self.bus_route_service.handle_bus_route_data(content)
        self.bus_route_service.save_bus_route_data_to_db(result)

    def test_save_station_list_to_db(self):
        with open(dirname(__file__) + '/resource/test_bus_route_service.xml', encoding='utf-8') as file:
            content = file.read()
        result = self.bus_route_service.handle_bus_route_data(content)
        self.bus_route_service.save_station_list_to_db(result)
        collection = mongodb_service.get_collection(config.mongodb, 'bus_station_all')
        data = collection.find_one({})
        assert data is not None
        assert len(data) > 0


if __name__ == '__main__':
    unittest.main()
