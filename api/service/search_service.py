from api.model.search_result import SearchResult
from api.service.bus_route_service import BusRouteService
from api.service.bus_station_service import BusStationService


class SearchService(object):
	TYPE_STATION = "0001"
	TYPE_ROUTE = "0002"

	def __init__(self):
		self.bus_route_service = BusRouteService()
		self.bus_station_service = BusStationService()

	def search(self, keywords, types: str, page, offset):
		search_station = False
		search_route = False
		if types is not None:
			if types.find('|'):
				types = types.split('|')
				for search_type in types:
					if search_type == self.TYPE_STATION:
						search_station = True
					elif search_type == self.TYPE_ROUTE:
						search_route = True
			else:
				if types == self.TYPE_STATION:
					search_station = True
				elif types == self.TYPE_ROUTE:
					search_route = True
		else:
			search_station = True
			search_route = True

		search_list = []
		name_list = []
		if search_route:
			route_list = self.bus_route_service.fuzzy_query_bus_route_by_name(keywords, page=page, offset=offset)
			for route in route_list:
				if route.route_name not in name_list:
					name_list.append(route.route_name)
				else:
					continue

				search_result = SearchResult()
				search_result.name = route.route_name
				search_result.type = self.TYPE_ROUTE
				search_list.append(search_result)

		if search_station:
			station_list = self.bus_station_service.fuzzy_query_bus_station_by_name(keywords, page=page, offset=offset)
			for station in station_list:
				if station.name not in name_list:
					name_list.append(station.name)
				else:
					continue

				search_result = SearchResult()
				search_result.name = station.name
				search_result.type = self.TYPE_STATION
				search_list.append(search_result)

		return search_list
