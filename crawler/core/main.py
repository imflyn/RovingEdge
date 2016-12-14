from twisted.internet import defer, reactor

from crawler.service.bus_route_service import BusRouteService


def crawl_bus_route(result):
    bus_route_service = BusRouteService()
    bus_route_service.crawl_bus_route_data()


deferred = defer.Deferred()
deferred.addCallback(crawl_bus_route)
deferred.callback('')
reactor.run()
