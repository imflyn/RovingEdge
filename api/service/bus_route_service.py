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
