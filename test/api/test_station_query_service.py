import unittest
from os.path import dirname

from api.service.bus_station_service import BusStationService


class TestStationQueryService(unittest.TestCase):
    def setUp(self):
        self.bus_station_service = BusStationService()
        pass

    def test_empty_html(self):
        result = self.bus_station_service.handle_html_data("")
        assert result is not None
        assert len(result) == 0

        result = self.bus_station_service.handle_html_data(None)
        assert result is not None
        assert len(result) == 0

    def test_empty_path(self):
        result = self.bus_station_service.handle_html_data("<table><tr></tr></table>")
        assert result is not None
        assert len(result) == 0

        result = self.bus_station_service.handle_html_data("asjdklasd")
        assert result is not None
        assert len(result) == 0

    def test_content(self):
        with open(dirname(__file__) + '/resource/test_bus_query.html', encoding='utf-8') as file:
            content = file.read()
        result = self.bus_station_service.handle_html_data(content)
        print(result)
        assert result is not None
        assert len(result) > 0

    def test_crawl_station_data(self):
        result = self.bus_station_service.crawl_station_data('火车站')
        print(result)
        assert result is not None
        assert len(result) > 0


if __name__ == '__main__':
    unittest.main()
