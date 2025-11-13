# scraper.py
from typing import List, Tuple
from .client import DoubanClient
from .parsers import TopListParser, DetailParser
from .domain import Movie

class DoubanTopScraper:
    def __init__(self, client: DoubanClient):
        self.client = client
        self.list_parser = TopListParser()
        self.detail_parser = DetailParser()

    def fetch_list(self, url: str) -> List[Tuple[str, str]]:
        html = self.client.get(url)
        return self.list_parser.parse_list(html)

    def fetch_detail(self, url: str) -> Movie:
        html = self.client.get(url)
        return self.detail_parser.parse_detail(html, url)
