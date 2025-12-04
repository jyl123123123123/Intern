# models.py
from sqlalchemy import (
    Column, String, Integer, Float, DateTime, Text, DECIMAL
)
from sqlalchemy.orm import deferred
from datetime import datetime
from .db import Base

class MovieORM(Base):
    __tablename__ = "movies"

    movie_id     = Column(String(20), primary_key=True)
    title_cn     = Column(String(255), nullable=False)
    title_orig   = Column(String(255))
    year         = Column(Integer)
    release_date = Column(String(20))
    runtime_min  = Column(Integer)
    rating_avg   = Column(DECIMAL(3,1), nullable=False)
    rating_count = Column(Integer, nullable=False)
    rating_5     = Column(DECIMAL(5,2))
    rating_4     = Column(DECIMAL(5,2))
    rating_3     = Column(DECIMAL(5,2))
    rating_2     = Column(DECIMAL(5,2))
    rating_1     = Column(DECIMAL(5,2))
    poster_url   = Column(String(500))
    summary      = Column(Text)
    source_url   = Column(String(500), nullable=False, unique=True)
    crawl_time   = Column(DateTime, nullable=False, default=datetime.utcnow)
    hash_sig     = Column(String(32))
