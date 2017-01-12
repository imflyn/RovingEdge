from flask import jsonify


class Converter(object):
	def __init__(self):
		self.converter = JsonConverter()

	def convert(self, list_data):
		return self.converter.convert(list_data)


class JsonConverter(object):
	def convert(self, list_data):
		return jsonify([obj.__dict__ for obj in list_data])


def convert_to_builtin_type(obj):
	d = {}
	d.update(obj.__dict__)
	return d
