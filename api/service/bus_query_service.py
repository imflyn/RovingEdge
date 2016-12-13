from lxml import etree
from lxml.etree import XMLSyntaxError
from lxml.etree import XPathEvalError

from api.model.bus_station import BusStation


class BusQueryService(object):
	def __init__(self):
		pass

	def handle_html_data(self, content) -> []:
		try:
			html = etree.HTML(content)
		except XMLSyntaxError:
			return []
		except ValueError:
			return []

		try:
			content_list = html.xpath("//span[@id='MainContent_DATA']//table//tr")
		except XPathEvalError:
			return []

		station_list = []
		for index, content_item in enumerate(content_list):
			if index == 0:
				continue

			name = content_item.getchildren()[0].xpath('a')[0].text
			number = content_item.getchildren()[1].text
			area = content_item.getchildren()[2].text
			road = content_item.getchildren()[3].text
			road_segment = content_item.getchildren()[4].text
			road_direction = content_item.getchildren()[5].text

			bus_station = BusStation()
			bus_station.name = name
			bus_station.number = number
			bus_station.area = area
			bus_station.road = road
			bus_station.road_segment = road_segment
			bus_station.road_direction = road_direction
			station_list.append(bus_station)

		return station_list
