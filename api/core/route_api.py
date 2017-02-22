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

	# /routes/{route_id}?name={name}&fuzzy=true
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument('name', type=str)
		parser.add_argument('fuzzy', type=str)
		args = parser.parse_args()
		route_name = args['name']
		fuzzy = args['fuzzy']

		if route_name is None:
			return make_response('', 404)

		if fuzzy and str(fuzzy).lower() == 'true':
			method = self.bus_route_service.fuzzy_query_bus_route_by_name
		else:
			method = self.bus_route_service.query_bus_route_by_name
		route_list = method(route_name)
		json = self.converter.convert(route_list)
		return make_response(json, 200)
