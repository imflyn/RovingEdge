from crawler.service.bus_route_service import BusRouteService


def crawl_bus_route():
	bus_route_service = BusRouteService()
	bus_route_list = bus_route_service.crawl_bus_route_data()
	return bus_route_list


def crawl_bus_station():

	pass


if __name__ == '__main__':
	crawl_bus_route()
	crawl_bus_station()
