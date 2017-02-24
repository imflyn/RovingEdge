from lxml import etree

from common import mongodb_service
from common import utils, log
from crawler.core import config
from crawler.core import constants
from crawler.model.bus_route import BusRoute


class BusRouteService(object):
    TABLE_BUS_ROUTE = 'bus_route'
    TABLE_BUS_STATION_ALL = 'bus_station_all'

    def __init__(self):
        pass

    def request_bus_route_data(self):
        response = utils.http_get(constants.URL_BUS_ROUTE, timeout=60)
        return response.text

    def handle_bus_route_data(self, xml_content):
        xml = etree.XML(xml_content)
        content_list = xml.xpath("//LPLine")
        bus_route_list = []
        for content_item in content_list:
            bus_route = BusRoute()
            bus_route.id = utils.get_uuid()
            bus_route.GUID = content_item.xpath('LPGUID')[0].text.lower()
            bus_route.route_name = content_item.xpath('LPLineName')[0].text
            bus_route.start_station = content_item.xpath('LPFStdName')[0].text
            bus_route.end_station = content_item.xpath('LPEStdName')[0].text
            bus_route.start_time = content_item.xpath('LPFStdFTime')[0].text
            bus_route.end_time = content_item.xpath('LPFStdETime')[0].text
            bus_route.peak_departure_interval = content_item.xpath('LPIntervalH')[0].text
            bus_route.low_departure_interval = content_item.xpath('LPIntervalN')[0].text
            bus_route.direction = content_item.xpath('LPDirection')[0].text
            pass_way = content_item.xpath('LPLineDirect')[0].text
            pass_way = utils.replace_number_symbol(pass_way)
            if pass_way is not None and not len(pass_way) == 0:
                pass_way = pass_way.replace('\n', '')
                bus_route.pass_way = pass_way.split('->')
            stations = content_item.xpath('LPStandName')[0].text
            stations = utils.replace_number_symbol(stations)
            if stations is not None and not len(stations) == 0:
                stations = stations.replace('\n', '')
                bus_route.stations = stations.split('、')
                bus_route.station_number = len(bus_route.stations)
            bus_route_list.append(bus_route)
        return bus_route_list

    def save_bus_route_data_to_db(self, bus_route_list):
        collection = mongodb_service.get_collection(config.mongodb, self.TABLE_BUS_ROUTE)
        data = []
        for bus_route in bus_route_list:
            data.append(bus_route.__dict__)
        # 删除整个表的数据再批量插入
        mongodb_service.delete_all_data(collection)
        log.info('爬取公交线路-->删除数据库中原有数据成功')
        mongodb_service.insert_all(collection, data)
        log.info('爬取公交线路-->数据插入数据库成功')
        self.handler_error_data(collection)
        log.info('爬取公交线路-->修改部分错误数据成功')

    def crawl_bus_route_data(self) -> []:
        log.info('爬取公交线路开始')
        try:
            bus_route_xml = self.request_bus_route_data()
            log.info('爬取公交线路XML成功')
            bus_route_list = self.handle_bus_route_data(bus_route_xml)
            log.info('处理公交线路数据成功')
            self.save_bus_route_data_to_db(bus_route_list)
            log.info('爬取公交线路成功')
            bus_station_list = self.save_station_list_to_db(bus_route_list)
            return bus_station_list
        except Exception as e:
            log.info('爬取公交线路失败')
            log.error(e)

    def save_station_list_to_db(self, bus_route_list):
        log.info('爬取公交线路-->去除重复公交站台开始')
        bus_station_list = []
        for bus_route in bus_route_list:
            bus_station_list.extend(bus_route.stations)
        bus_station_list = list(set(bus_station_list))
        log.info('爬取公交线路-->去除重复公交站台成功')
        collection = mongodb_service.get_collection(config.mongodb, self.TABLE_BUS_STATION_ALL)
        mongodb_service.delete_all_data(collection)
        log.info('爬取公交线路-->删除旧公交站台集合数据成功')
        mongodb_service.insert(collection, {'bus_station_list': bus_station_list})
        log.info('爬取公交线路-->保存公交站台集合数据成功')
        return bus_station_list

    def handler_error_data(self, collection):
        collection.update_one({'GUID': 'aaaaaaaa-aaaa-aaaa-aaaa-000000000001'}, {"$set": {'GUID': '778d674e-b483-4a13-9aaf-d1acb705d10d'}})
        collection.update_one({'GUID': 'aaaaaaaa-aaaa-aaaa-aaaa-000000000002'}, {"$set": {'GUID': '4f63f3a0-c003-43b1-b9a1-88240efb0800'}})
        collection.update_one({'GUID': 'aaaaaaaa-aaaa-aaaa-aaaa-000000000003'}, {"$set": {'GUID': '96aa2ec5-031a-4e84-a358-611f08f07947'}})
        collection.update_one({'GUID': 'aaaaaaaa-aaaa-aaaa-aaaa-000000000004'}, {"$set": {'GUID': '374cb92a-5886-432b-a1fc-1f997ff43662'}})
        collection.update_one({'GUID': 'aaaaaaaa-aaaa-aaaa-aaaa-000000000005'}, {"$set": {'GUID': ''}})
        collection.update_one({'GUID': 'aaaaaaaa-aaaa-aaaa-aaaa-000000000006'}, {"$set": {'GUID': 'e7d3789b-fcef-42de-ba49-d0e9a42f452a'}})
        collection.update_one({'GUID': 'aaaaaaaa-aaaa-aaaa-aaaa-000000000007'}, {"$set": {'GUID': '1b414ade-6468-4242-ad36-c8ac3e13a2b7'}})
        collection.update_one({'GUID': 'aaaaaaaa-aaaa-aaaa-aaaa-000000000008'}, {"$set": {'GUID': '084ef4a4-e549-46a0-8aff-5c77092745ae'}})
