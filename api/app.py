from flask import Flask
from flask.ext.restful import Api

from api.core.station_api import StationApi

app = Flask(__name__)
api = Api(app)
api.add_resource(StationApi, StationApi.QUERY_STATION_BY_NAME)

if __name__ == '__main__':
    app.run(debug=True)
