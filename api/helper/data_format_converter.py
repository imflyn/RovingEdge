from flask import jsonify


class Converter(object):
    def __init__(self):
        self.converter = JsonConverter()

    def convert(self, list_data):
        return self.converter.convert(list_data)


class JsonConverter(object):
    def convert(self, list_data):
        return jsonify([obj.__dict__ for obj in list_data])
