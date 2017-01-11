from flask import Flask
from flask_restful import Api

from api.core.real_time_station_api import RealTimeStationApi
from api.core.route_api import RouteApi
from api.core.station_api import StationApi

app = Flask(__name__)
api = Api(app)
api.add_resource(StationApi, StationApi.QUERY_STATION_BY_NAME)
api.add_resource(RouteApi, RouteApi.QUERY_ROUTE_BY_NAME)
api.add_resource(RealTimeStationApi, RealTimeStationApi.QUERY_REAL_TIME_STATION_BY_NAME)

if __name__ == '__main__':
	app.run(debug=True)
