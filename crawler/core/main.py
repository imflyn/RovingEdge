import os
import sys
from os.path import dirname

sys.path.append(dirname(dirname(dirname(__file__))))

import threading
import time
from concurrent.futures import ThreadPoolExecutor

from schedule import Scheduler

from common import log
from crawler.core import config
from crawler.service.bus_route_service import BusRouteService
from crawler.service.bus_station_service import BusStationService


def crawl_bus_route():
    bus_route_service = BusRouteService()
    bus_route_list = bus_route_service.crawl_bus_route_data()
    return bus_route_list


def crawl_bus_station(bus_station_list):
    pool = ThreadPoolExecutor(4)
    futures = []

    def callbacks_finished():
        callbacks_finished.count += 1
        log.info("爬取进度-->({index}/{count})".format(index=callbacks_finished.count, count=len(bus_station_list)))
        if callbacks_finished.count == len(bus_station_list):
            os._exit(0)

    callbacks_finished.count = 0

    bus_station_service = BusStationService()

    def crawl(bus_station):
        bus_station_service.crawl_bus_station_data(bus_station)
        callbacks_finished()

    for bus_station in bus_station_list:
        futures.append(pool.submit(crawl, bus_station))


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
