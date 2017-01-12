from flask import make_response
from flask_restful import reqparse

from api.core.base_resource import BaseResource
from api.helper.data_format_converter import Converter
from api.service.bus_station_service import BusStationService


class StationApi(BaseResource):
	QUERY_STATION_BY_NAME = '/station'

	def __init__(self):
		self.bus_station_service = BusStationService()
		self.converter = Converter()

	# /station?name={0}
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument('name', type=str)
		args = parser.parse_args()
		route_name = args['name']

		station_list = self.bus_station_service.query_bus_station_by_name(route_name)
		json = self.converter.convert(station_list)
		return make_response(json, 200)
