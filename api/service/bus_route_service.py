from api import config
from api.model.bus_route import BusRoute
from common import mongodb_service


class BusRouteService(object):
	TABLE_BUS_ROUTE = 'bus_route'

	def __init__(self):
		self.bus_route_collection = mongodb_service.get_collection(config.mongodb, self.TABLE_BUS_ROUTE)

	def query_bus_route_by_name(self, route_name):
		route_list = []
		route_cursor = self.bus_route_collection.find({'route_name': route_name})
		for route_dict in route_cursor:
			route = BusRoute.create(route_dict)
			route_list.append(route)
		return route_list

	def fuzzy_query_bus_route_by_name(self, route_name, **kwargs):
		try:
			page = kwargs['page']
		except KeyError:
			page = None
		try:
			offset = kwargs['offset']
		except KeyError:
			offset = None
		route_list = []
		if (isinstance(page, int) and page >= 0) and (isinstance(offset, int) and offset > 0):
			route_cursor = self.bus_route_collection.find({'route_name': {'$regex': route_name}}).skip(page).limit(offset).sort('route_name')
		else:
			route_cursor = self.bus_route_collection.find({'route_name': {'$regex': route_name}}).sort('route_name')
		for route_dict in route_cursor:
			route = BusRoute.create(route_dict)
			route_list.append(route)

		route_list.sort(key=lambda x: (x.route_name.startswith(route_name)), reverse=True)
		return route_list
