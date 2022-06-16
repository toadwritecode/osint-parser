from ..abstract_parser import AbstractParser


class ShodanParser(AbstractParser):

    def __init__(self, url):
        self.api_url = url

    def request(self):
        self._request()

    def perform(self):
        self._perform()

    def parse(self):
        pass
