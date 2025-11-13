# main.py
import logging
from .db import SessionLocal
from .client import DoubanClient
from .scraper import DoubanTopScraper
from .repository import SqlAlchemyMovieRepository
from .pipeline import IngestionPipeline

def top250_pages_first_100():
    base = "https://movie.douban.com/top250?start={}&filter="
    return [base.format(i) for i in (0, 25, 50, 75)]

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
    client = DoubanClient()
    scraper = DoubanTopScraper(client)

    with SessionLocal() as session:
        repo = SqlAlchemyMovieRepository(session)
        pipe = IngestionPipeline(scraper, repo)
        total = pipe.run_pages(top250_pages_first_100(), per_page_limit=25)
        session.commit()
        logging.info("Done. Insert/Update total=%d", total)
