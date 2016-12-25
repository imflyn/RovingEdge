import unittest

from api.service.bus_station_service import BusStationService


class TestBusStationService(unittest.TestCase):
    def setUp(self):
        self.bus_station_service = BusStationService()
        pass


if __name__ == '__main__':
    unittest.main()
