# repository.py
import hashlib
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from .models import MovieORM
from .domain import Movie

def movie_hash(m: Movie) -> str:
    raw = "|".join([
        m.movie_id, m.title_cn or "", str(m.year or ""),
        str(m.rating_avg or ""), str(m.rating_count or ""),
        str(m.runtime_min or "")
    ]).encode("utf-8")
    return hashlib.md5(raw).hexdigest()

class SqlAlchemyMovieRepository:
    def __init__(self, session: Session):
        self.session = session

    def upsert(self, m: Movie):
        sig = movie_hash(m)
        obj = self.session.get(MovieORM, m.movie_id)
        if obj is None:
            obj = MovieORM(
                movie_id=m.movie_id,
                title_cn=m.title_cn,
                title_orig=m.title_orig,
                year=m.year,
                release_date=m.release_date,
                runtime_min=m.runtime_min,
                rating_avg=m.rating_avg,
                rating_count=m.rating_count,
                poster_url=m.poster_url,
                summary=(m.summary or "")[:2000],
                source_url=m.source_url,
                crawl_time=m.crawl_time,
                hash_sig=sig
            )
            self.session.add(obj)
        else:
            if obj.hash_sig != sig:
                obj.title_cn = m.title_cn
                obj.title_orig = m.title_orig
                obj.year = m.year
                obj.release_date = m.release_date
                obj.runtime_min = m.runtime_min
                obj.rating_avg = m.rating_avg
                obj.rating_count = m.rating_count
                obj.poster_url = m.poster_url
                obj.summary = (m.summary or "")[:2000]
                obj.source_url = m.source_url
                obj.crawl_time = m.crawl_time
                obj.hash_sig = sig
