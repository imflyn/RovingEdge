from api import config
from common import mongodb_service


class BusRouteService(object):
	TABLE_BUS_ROUTE = 'bus_route'

	def __init__(self):
		self.bus_route_collection = mongodb_service.get_collection(config.mongodb, self.TABLE_BUS_ROUTE)

	def query_bus_route_by_name(self, route_name):
		self.bus_route_collection.find_one({'route_name': ''})
