from flask_restful import Resource, reqparse

from api.helper.data_format_converter import Converter
from api.service.bus_station_service import BusStationService


class RealTimeStationApi(Resource):
	QUERY_REAL_TIME_STATION_BY_NAME = '/real_time_station'

	def __init__(self):
		self.bus_station_service = BusStationService()
		self.converter = Converter()

	# /real_time_station/
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument('station', type=str)
		args = parser.parse_args()
		station = args['station']

		station_list = self.bus_station_service.query_bus_station_by_name(station)
		for station in station_list:
			self.bus_station_service.get_real_time_station_data(station)
