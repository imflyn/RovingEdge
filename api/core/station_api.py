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
		parser.add_argument('fuzzy', type=str)
		args = parser.parse_args()
		state_name = args['name']
		fuzzy = args['fuzzy']

		if state_name is None:
			return make_response('', 404)

		if fuzzy and str(fuzzy).lower() == 'true':
			method = self.bus_station_service.fuzzy_query_bus_station_by_name
		else:
			method = self.bus_station_service.query_bus_station_by_name
		station_list = method(state_name)
		json = self.converter.convert(station_list)
		return make_response(json, 200)
