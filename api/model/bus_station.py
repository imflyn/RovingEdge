class BusStation(object):
    def __init__(self):
        self.id = ""
        self.name = ""  # 团结桥北
        self.number = ""  # DSH
        self.area = ""  # 沧浪区
        self.road = ""  # 人民路
        self.road_segment = ""  # 南门路-南环路
        self.road_direction = ""  # 西

    @classmethod
    def create(cls, station_dict):
        station = BusStation()
        station.id = station_dict['id']
        station.name = station_dict['name']
        station.number = station_dict['number']
        station.area = station_dict['area']
        station.road = station_dict['road']
        station.road_segment = station_dict['road_segment']
        station.road_direction = station_dict['road_direction']
        return station
