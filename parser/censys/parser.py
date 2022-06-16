import os
import re

from .response import CensysResponse
from ..abstract_parser import AbstractParser


class CensysParser(AbstractParser):

    response: CensysResponse

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.response = kwargs.get('response')
        self.api_url = os.environ.get('CENSYS_API_URL')

    def request(self) -> AbstractParser:
        self._request()
        return CensysParser(http_response=self.http_response)

    def perform(self) -> AbstractParser:
        self._perform()
        return CensysParser(http_response=self.http_response, html=self.html)

    def parse(self) -> AbstractParser:
        self._parse()
        return CensysParser(http_response=self.http_response, html=self.html, response=self.response)

    def export(self):
        self._export(self.response)

    def _parse(self):
        host = self._get_host()
        technologies = self.__get_tech_stack()
        protocols = self.__get_protocols()
        titles = self.__get_titles()
        source = self.api_url

        self.response = CensysResponse(
            host=host,
            technologies=technologies,
            protocols=protocols,
            titles=titles,
            source=source
        )

    def _get_host(self) -> str:
        indexes = [i.start() for i in re.finditer(r"/", self.api_url)]
        return self.api_url[indexes[3] + 1:]

    def __get_tech_stack(self) -> str:
        unique_technologies = []

        elements = self.html.find_all('h5', attrs={'class': 'software-header'})
        for element in elements:
            tech = ' '.join([el for el in element.find_next('span').text.replace('\n', '').split(' ') if el != ''])\
                .capitalize()

            if tech not in unique_technologies:
                unique_technologies.append(tech)

        return ', '.join(unique_technologies)

    def __get_protocols(self) -> str:
        elements = self.html.find_all('dt')
        for element in elements:
            if element.text.lower() == 'protocols':
                protocols = [el.strip() for el in element.find_next('dd').text.split(',')]
                return '; '.join(protocols)

    def __get_titles(self) -> str:
        titles = []
        elements = self.html.find_all('h4')
        for element in elements:
            if element.text.lower() == 'details':
                table = element.find_next('dl')
                columns = table.find_all('dt')
                for column in columns:
                    if column.text.lower() in ['html title', 'banner']:
                        text = column.find_next('dd').text.strip()
                        titles.append(text)
        return '; '.join(titles)
