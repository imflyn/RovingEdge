import unittest
from os.path import dirname

from api.service.bus_query_service import BusQueryService


class TestBusQueryService(unittest.TestCase):
	def setUp(self):
		self.bus_query_service = BusQueryService()
		pass

	def test_empty_html(self):
		result = self.bus_query_service.handle_html_data("")
		assert result is not None
		assert len(result) == 0

		result = self.bus_query_service.handle_html_data(None)
		assert result is not None
		assert len(result) == 0

	def test_empty_path(self):
		result = self.bus_query_service.handle_html_data("<table><tr></tr></table>")
		assert result is not None
		assert len(result) == 0

		result = self.bus_query_service.handle_html_data("asjdklasd")
		assert result is not None
		assert len(result) == 0

	def test_content(self):
		with open(dirname(__file__) + '/resource/test_bus_query.html', encoding='utf-8') as file:
			content = file.read()
		result = self.bus_query_service.handle_html_data(content)
		print(result)
		assert result is not None
		assert len(result) > 0


if __name__ == '__main__':
	unittest.main()
