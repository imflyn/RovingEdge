from flask import make_response
from flask_restful import reqparse

from api.core.base_resource import BaseResource
from api.helper.data_format_converter import Converter
from api.service.bus_route_service import BusRouteService


class RouteApi(BaseResource):
	QUERY_ROUTE_BY_NAME = '/route'

	def __init__(self):
		self.bus_route_service = BusRouteService()
		self.converter = Converter()

	# /routes/{route_id}?name={name}
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument('name', type=str)
		args = parser.parse_args()
		route_name = args['name']

		route_list = self.bus_route_service.query_bus_route_by_name(route_name)
		json = self.converter.convert(route_list)
		return make_response(json, 200)
