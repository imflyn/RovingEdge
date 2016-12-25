class BusRoute(object):
    def __init__(self):
        self.id = ""
        self.GUID = ""
        self.route_name = ""  # 线路名称
        self.start_station = ""  # 首站
        self.end_station = ""  # 末站
        self.start_time = ""  # 首班车时间
        self.end_time = ""  # 末班车时间
        self.peak_departure_interval = ""  # 高峰期发车间隔
        self.low_departure_interval = ""  # 低峰期发车间隔
        self.direction = ""  # 方向
        self.pass_way = []  # 途经
        self.stations = []  # 停靠站点
        self.station_number = 0  # 站数

    @classmethod
    def create(cls, route_dict):
        route = BusRoute()
        route.id = route_dict['id']
        route.GUID = route_dict['GUID']
        route.route_name = route_dict['route_name']
        route.start_station = route_dict['start_station']
        route.end_station = route_dict['end_station']
        route.start_time = route_dict['start_time']
        route.end_time = route_dict['end_time']
        route.peak_departure_interval = route_dict['peak_departure_interval']
        route.low_departure_interval = route_dict['low_departure_interval']
        route.direction = route_dict['direction']
        route.pass_way = route_dict['pass_way']
        route.stations = route_dict['stations']
        route.station_number = route_dict['station_number']
        return route
