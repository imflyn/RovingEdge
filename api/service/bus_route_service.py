import requests
from lxml import etree
from lxml.etree import XMLSyntaxError
from lxml.etree import XPathEvalError

from api import config
from api.model.bus_route import BusRoute
from api.model.real_time_route import RealTimeRoute
from common import mongodb_service, log


class BusRouteService(object):
    TABLE_BUS_ROUTE = 'bus_route'

    def __init__(self):
        self.bus_route_collection = mongodb_service.get_collection(config.mongodb, self.TABLE_BUS_ROUTE)

    def query_bus_route_by_name(self, route_name):
        route_list = []
        route_cursor = self.bus_route_collection.find({'route_name': route_name})
        for route_dict in route_cursor:
            route = BusRoute.create(route_dict)
            route_list.append(route)
        return route_list

    def fuzzy_query_bus_route_by_name(self, route_name, **kwargs):
        try:
            page = kwargs['page']
        except KeyError:
            page = None
        try:
            offset = kwargs['offset']
        except KeyError:
            offset = None
        route_list = []
        if (isinstance(page, int) and page >= 0) and (isinstance(offset, int) and offset > 0):
            route_cursor = self.bus_route_collection.find({'route_name': {'$regex': '^' + route_name}}).skip(page).limit(offset).sort('route_name')
        else:
            route_cursor = self.bus_route_collection.find({'route_name': {'$regex': '^' + route_name}}).sort('route_name')
        for route_dict in route_cursor:
            route = BusRoute.create(route_dict)
            route_list.append(route)

        route_list.sort(key=lambda x: (x.route_name.startswith(route_name)), reverse=True)
        return route_list

    def get_real_time_route_data(self, route, route_id):
        html = self.request_real_time_route_data(route, route_id)
        real_time_bus_list = self.handle_real_time_route_data(html, route)
        return real_time_bus_list

    def request_real_time_route_data(self, route, route_id):
        url = 'http://www.szjt.gov.cn/apts/APTSLine.aspx?LineGuid=' + route_id + '&LineInfo=' + route
        try:
            response = requests.post(url, timeout=20)
        except Exception as e:
            log.error(e)
            return None
        if response is None:
            return None
        return response.text

    def handle_real_time_route_data(self, content, route) -> []:
        try:
            html = etree.HTML(content)
        except XMLSyntaxError as e:
            log.error(e)
            return []
        except ValueError as e:
            log.error(e)
            return []
        try:
            content_list = html.xpath("//span[@id='MainContent_DATA']//table//tr")
        except XPathEvalError as e:
            log.error(e)
            return []

        real_time_route_list = []
        for index, content_item in enumerate(content_list):
            if index == 0:
                continue

            station = content_item.getchildren()[0].xpath('a')[0].text
            number = content_item.getchildren()[1].text
            license = content_item.getchildren()[2].text
            update_time = content_item.getchildren()[3].text

            real_time_route = RealTimeRoute()
            real_time_route.station = station
            real_time_route.number = number
            real_time_route.license = license
            real_time_route.update_time = update_time
            real_time_route.route = route
            real_time_route_list.append(real_time_route)
        return real_time_route_list
