from flask import make_response
from flask_restful import reqparse

from api.core.base_resource import BaseResource
from api.helper.data_format_converter import Converter
from api.service.bus_route_service import BusRouteService


class RealTimeRouteApi(BaseResource):
    QUERY_REAL_TIME_ROUTE_BY_NAME = '/real_time_route'

    def __init__(self):
        self.bus_route_service = BusRouteService()
        self.converter = Converter()

    # /real_time_route?route=1&id=
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('route', type=str)
        parser.add_argument('id', type=str)
        args = parser.parse_args()

        route = None
        route_id = None
        try:
            route = args['route']
        except KeyError:
            pass
        try:
            route_id = args['id']
        except KeyError:
            pass

        if route is None or route_id is None:
            return make_response('', 404)

        real_time_route_data = self.bus_route_service.get_real_time_route_data(route, route_id)
        if real_time_route_data is None or len(real_time_route_data) == 0:
            return make_response('', 404)

        return make_response(self.converter.convert(real_time_route_data), 200)
