# domain.py
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Movie:
    movie_id: str
    title_cn: str
    title_orig: Optional[str]
    year: Optional[int]
    rating_avg: Optional[float]
    rating_count: Optional[int]
    runtime_min: Optional[int]
    source_url: str
    crawl_time: datetime
    release_date: Optional[str] = None
    poster_url: Optional[str] = None
    summary: Optional[str] = None