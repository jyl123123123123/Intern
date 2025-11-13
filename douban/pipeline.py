# pipeline.py
import logging
from typing import Iterable
from .repository import SqlAlchemyMovieRepository
from .scraper import DoubanTopScraper

class IngestionPipeline:
    def __init__(self, scraper: DoubanTopScraper, repo: SqlAlchemyMovieRepository):
        self.scraper = scraper
        self.repo = repo

    def run_pages(self, list_urls: Iterable[str], per_page_limit: int = 25):
        total = 0
        for url in list_urls:
            pairs = self.scraper.fetch_list(url)
            logging.info("List %s -> %d items", url, len(pairs))
            for i, (_, detail_url) in enumerate(pairs):
                if i >= per_page_limit:
                    break
                movie = self.scraper.fetch_detail(detail_url)
                self.repo.upsert(movie)
                total += 1
        return total
