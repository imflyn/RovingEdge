from flask import json, jsonify
from flask import make_response
from flask_restful import reqparse

from api.core.base_resource import BaseResource
from api.core.error.real_time_station_not_found_error import RealTimeStationNotFoundError
from api.helper.data_format_converter import Converter, convert_to_builtin_type
from api.service.bus_station_service import BusStationService


class RealTimeStationApi(BaseResource):
    QUERY_REAL_TIME_STATION_BY_NAME = '/real_time_station'

    def __init__(self):
        self.bus_station_service = BusStationService()
        self.converter = Converter()

    # /real_time_station/station=独墅苑
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('station', type=str)
        args = parser.parse_args()
        station = args['station']

        real_time_bus_dict = {}
        station_list = self.bus_station_service.fuzzy_query_bus_station_by_name(station)
        for station in station_list:
            real_time_station_data = self.bus_station_service.get_real_time_station_data(station.number)
            if real_time_station_data is None or len(real_time_station_data) == 0:
                continue
            real_time_bus_dict[station.number] = real_time_station_data

        if real_time_bus_dict is None or len(real_time_bus_dict) == 0:
            error = RealTimeStationNotFoundError()
            error.field_value = station
            return make_response(jsonify(error.__dict__), 404)

        return make_response(json.dumps(real_time_bus_dict, default=convert_to_builtin_type, ensure_ascii=False, separators=(', ', ': ')), 200)

    # /real_time_station?number=GKE
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('number', type=str)
        args = parser.parse_args()

        number = None
        try:
            number = args['number']
        except KeyError:
            pass

        real_time_bus_list = self.bus_station_service.get_real_time_station_data(number)
        if real_time_bus_list is None or len(real_time_bus_list) == 0:
            return make_response('', 404)

        return make_response(self.converter.convert(real_time_bus_list), 200)
