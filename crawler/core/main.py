import threading
import time

from schedule import Scheduler
from twisted.internet import defer
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks

from common import log
from crawler.core import config
from crawler.service.bus_route_service import BusRouteService
from crawler.service.bus_station_service import BusStationService


def crawl_bus_route():
    bus_route_service = BusRouteService()
    bus_route_list = bus_route_service.crawl_bus_route_data()
    return bus_route_list


def crawl_bus_station(bus_station_list):
    def callbacks_finished(_):
        callbacks_finished.count += 1
        log.info("爬取进度-->({index}/{count})".format(index=callbacks_finished.count, count=len(bus_station_list)))
        if callbacks_finished.count == len(bus_station_list):
            reactor.stop()

    callbacks_finished.count = 0

    def crawl(bus_station, callback):
        bus_station_service = BusStationService()
        bus_station_service.crawl_bus_station_data(bus_station)
        callback('')

    @inlineCallbacks
    def crawl_bus_station():
        for bus_station in bus_station_list:
            bus_defer = defer.Deferred()
            bus_defer.addBoth(callbacks_finished)
            reactor.callInThread(crawl, bus_station, bus_defer.callback)
            yield bus_defer

    reactor.callWhenRunning(crawl_bus_station)
    reactor.run()


if __name__ == '__main__':
    def task():
        from crawler.proxy.proxy_pool import proxy_pool
        if config.USE_PROXY:
            proxy_pool.start()
        else:
            proxy_pool.drop_proxy()


    def thread_task():
        schedule = Scheduler()
        schedule.every(30).minutes.do(task)

        while True:
            schedule.run_pending()
            time.sleep(1)


    thread = threading.Thread(target=thread_task)
    thread.start()
    task()
    bus_station_list = crawl_bus_route()
    crawl_bus_station(bus_station_list)
