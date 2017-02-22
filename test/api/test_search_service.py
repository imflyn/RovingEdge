import unittest

from api.service.search_service import SearchService


class TestBusRouteService(unittest.TestCase):
	def setUp(self):
		self.search_service = SearchService()

	def test_search_service(self):
		search_list = self.search_service.search(keywords='2', types=None, page=0, offset=0)
		assert len(search_list) > 0


if __name__ == '__main__':
	unittest.main()
