import json


class Converter(object):
    def __init__(self):
        self.converter = JsonConverter()

    def convert(self, list_data):
        return self.converter.convert(list_data)


class JsonConverter(object):
    def convert(self, list_data):
        return json.dumps([obj.__dict__ for obj in list_data], ensure_ascii=False)
