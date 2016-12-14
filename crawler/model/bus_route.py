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
