from api.core.error.error import Error


class RealTimeStationNotFoundError(Error):
	def __init__(self):
		super(RealTimeStationNotFoundError, self).__init__()
		self.error_code = 'REAL_TIME_STATION_NOT_FOUND'
		self.field_name = 'Station'
		self.field_value = ''
		self.cn = '暂无数据'
		self.en = 'Temporarily no data'
