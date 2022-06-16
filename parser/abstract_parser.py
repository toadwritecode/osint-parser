import xlsxwriter as xl
from abc import ABCMeta, abstractmethod
from requests import get, Response, HTTPError
from bs4 import BeautifulSoup


class AbstractParser(metaclass=ABCMeta):

    api_url: str
    http_response: Response
    html: BeautifulSoup

    DEFAULT_HTTP_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1'
    }

    def __init__(self, **kwargs):
        self.http_response = kwargs.get('http_response')
        self.html = kwargs.get('html')

    @abstractmethod
    def request(self):
        pass

    @abstractmethod
    def perform(self):
        pass

    @abstractmethod
    def parse(self):
        pass

    @abstractmethod
    def export(self):
        pass

    def _request(self):
        self.http_response = get(self.api_url, headers=self.DEFAULT_HTTP_HEADERS)

    def _perform(self):
        match self.http_response.headers:
            case {'Content-Type': 'text/html; charset=UTF-8'}:
                self._perform_html()
            case {'Content-Type': 'json; charset=UTF-8'}:
                self._perform_json()
            case _:
                raise HTTPError(f"Incorrect response type: {self.http_response.headers}")

    def _perform_html(self):
        html_content = self.http_response.content
        self.html = BeautifulSoup(html_content, features="html.parser")

    def _perform_json(self):
        pass

    @staticmethod
    def _export(response):
        response = response.dict()

        workbook = xl.Workbook('response.xlsx')
        worksheet = workbook.add_worksheet()

        row = 0
        for k, v in response.items():
            worksheet.write(row, 0, k)
            worksheet.write(row, 1, v)
            row += 1

        workbook.close()
