from flask.ext.restful import Resource, reqparse


class StationApi(Resource):
    QUERY_STATION_BY_NAME = '/station'

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        args = parser.parse_args()
        name = args['name']
        return name