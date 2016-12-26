from api import config
from api.model.bus_station import BusStation
from common import mongodb_service


class BusStationService(object):
    TABLE_BUS_STATION = 'bus_station'

    def __init__(self):
        self.bus_station_collection = mongodb_service.get_collection(config.mongodb, self.TABLE_BUS_STATION)

    def query_bus_station_by_name(self, station_name):
        station_list = []
        station_cursor = self.bus_station_collection.find({'name': station_name})
        for station_dict in station_cursor:
            route = BusStation.create(station_dict)
            station_list.append(route)
        return station_list
