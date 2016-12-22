import threading
import time

from schedule import Scheduler
from twisted.internet import reactor
from twisted.internet.defer import Deferred

from common import log
from crawler.core import config
from crawler.service.bus_route_service import BusRouteService
from crawler.service.bus_station_service import BusStationService


def crawl_bus_route():
	bus_route_service = BusRouteService()
	bus_route_list = bus_route_service.crawl_bus_route_data()
	return bus_route_list


def crawl_bus_station(bus_station_list):
	def crawl_bus_station(bus_station) -> Deferred:
		defer = Deferred()
		bus_station_service = BusStationService()
		bus_station_service.crawl_bus_station_data(bus_station)
		return defer

	def task():
		def callbacks_finished(_):
			callbacks_finished.count += 1
			log.info("爬取进度-->({index}/{count})".format(index=callbacks_finished.count, count=len(bus_station_list)))
			if callbacks_finished.count == len(bus_station_list):
				reactor.stop()

		callbacks_finished.count = 0

		for bus_station_entry in bus_station_list:
			defer = crawl_bus_station(bus_station_entry)
			defer.addBoth(callbacks_finished)
			defer.callback('')

	reactor.callWhenRunning(task)
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
