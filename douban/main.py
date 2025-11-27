# douban/main.py

import logging
from sqlalchemy import create_engine, text

from .db import engine, Base, SessionLocal
from .client import DoubanClient
from .scraper import DoubanTopScraper
from .repository import SqlAlchemyMovieRepository  
from .pipeline import IngestionPipeline


def init_db():
    """
    自动创建test数据库+创建所有表(如果不存在)
    """
    
    engine_root = create_engine(
        "mysql+pymysql://root:Rutgers123456@localhost:3306/",
        pool_pre_ping=True,
    )

    
    with engine_root.connect() as conn:
        conn.execute(
            text("CREATE DATABASE IF NOT EXISTS test CHARACTER SET utf8mb4;")
        )
        conn.commit()

    
    Base.metadata.create_all(engine)


def top250_pages_first_100():
    """
    生成 Top250 前 4 页的链接（共 100 条）
    """
    base = "https://movie.douban.com/top250?start={}&filter="
    return [base.format(i) for i in (0, 25, 50, 75)]


def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

    
    init_db()

    client = DoubanClient()
    scraper = DoubanTopScraper(client)

    
    with SessionLocal() as session:
        repo = SqlAlchemyMovieRepository(session)
        pipe = IngestionPipeline(scraper, repo)

        total = pipe.run_pages(top250_pages_first_100(), per_page_limit=25)
        session.commit()

        logging.info("Done. Insert/Update total=%d", total)


if __name__ == "__main__":
    main()
