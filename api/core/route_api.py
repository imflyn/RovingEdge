from flask.ext.restful import Resource, reqparse

from api.service.bus_route_service import BusRouteService


class RouteApi(Resource):
	QUERY_STATION_BY_NAME = '/route'

	def __init__(self):
		self.bus_route_service = BusRouteService()

	# /routes/{route_id}?name={name}
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument('name', type=str)
		args = parser.parse_args()
		route_name = args['name']

		self.bus_route_service

		return name
