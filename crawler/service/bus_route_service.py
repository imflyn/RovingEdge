from lxml import etree

from common import mongodb_service
from common import utils, log
from crawler.core import config
from crawler.core import constants
from crawler.model.bus_route import BusRoute


class BusRouteService(object):
    TABLE_NAME = 'bus_route'

    def __init__(self):
        pass

    def request_bus_route_data(self):
        response = utils.http_request(constants.URL_BUS_ROUTE, timeout=60)
        return response.text

    def handle_bus_route_data(self, xml_content):
        xml = etree.XML(xml_content)
        content_list = xml.xpath("//LPLine")
        bus_route_list = []
        for content_item in content_list:
            bus_route = BusRoute()
            bus_route.id = utils.get_uuid()
            bus_route.GUID = content_item.xpath('LPGUID')[0].text
            bus_route.route_name = content_item.xpath('LPLineName')[0].text
            bus_route.start_station = content_item.xpath('LPFStdName')[0].text
            bus_route.end_station = content_item.xpath('LPEStdName')[0].text
            bus_route.start_time = content_item.xpath('LPFStdFTime')[0].text
            bus_route.end_time = content_item.xpath('LPFStdETime')[0].text
            bus_route.peak_departure_interval = content_item.xpath('LPIntervalH')[0].text
            bus_route.low_departure_interval = content_item.xpath('LPIntervalN')[0].text
            bus_route.direction = content_item.xpath('LPDirection')[0].text
            pass_way = content_item.xpath('LPLineDirect')[0].text
            if pass_way is not None and not len(pass_way) == 0:
                pass_way = pass_way.replace('\n', '')
                bus_route.pass_way = pass_way.split('->')
            stations = content_item.xpath('LPStandName')[0].text
            if stations is not None and not len(stations) == 0:
                stations = stations.replace('\n', '')
                bus_route.stations = stations.split('、')
                bus_route.station_number = len(bus_route.stations)
            bus_route_list.append(bus_route)
        return bus_route_list

    def save_bus_route_data_to_db(self, bus_route_list):
        collection = mongodb_service.get_collection(config.mongodb, self.TABLE_NAME)
        data = []
        for bus_route in bus_route_list:
            data.append(bus_route.__dict__)
        # 删除整个表的数据再批量插入
        mongodb_service.delete_all_data(collection)
        mongodb_service.insert_all(collection, data)

    def crawl_bus_route_data(self):
        log.info('爬取公交线路开始')
        try:
            bus_route_xml = self.request_bus_route_data()
            bus_route_list = self.handle_bus_route_data(bus_route_xml)
            self.save_bus_route_data_to_db(bus_route_list)
            log.info('爬取公交线路成功')
        except Exception as e:
            log.info('爬取公交线路失败')
            log.error(e)
