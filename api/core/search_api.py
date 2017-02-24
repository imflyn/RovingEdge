from flask import make_response
from flask_restful import reqparse

from api.core.base_resource import BaseResource
from api.helper.data_format_converter import Converter
from api.service.search_service import SearchService


class SearchApi(BaseResource):
    SEARCH = '/search'

    def __init__(self):
        self.search_service = SearchService()
        self.converter = Converter()

    # /search?keyword={keyword}&types={types}&page={page}&offset={offset}
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('keyword', type=str)
        parser.add_argument('type', type=str)
        parser.add_argument('page', type=int)
        parser.add_argument('offset', type=int)
        args = parser.parse_args()
        keywords = args['keyword']
        types = None
        try:
            types = args['types']
        except KeyError:
            pass
        page = args['page']
        offset = args['offset']

        if not offset or isinstance(offset, int):
            offset = 0
        if not page or isinstance(page, int):
            page = 0

        if keywords is None or len(keywords) == 0:
            return make_response('', 404)

        search_result_list = self.search_service.search(keywords=keywords, types=types, page=page, offset=offset)
        json = self.converter.convert(search_result_list)
        return make_response(json, 200)
