# parsers.py
import re
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Tuple
from .domain import Movie

SUBJECT_ID_RE = re.compile(r"/subject/(\d+)/")

class TopListParser:
    def parse_list(self, html: str) -> List[Tuple[str, str]]:
        soup = BeautifulSoup(html, "lxml")
        items = []
        for a in soup.select("div.item div.pic a[href*='/subject/']"):
            href = a.get("href", "").strip()
            title = a.get("title") or (a.find("img").get("alt") if a.find("img") else "")
            if href:
                items.append((title.strip(), href))
        return items

class DetailParser:
    def _extract_id(self, url: str) -> str:
        m = SUBJECT_ID_RE.search(url)
        return m.group(1) if m else url

    def parse_detail(self, html: str, url: str) -> Movie:
        soup = BeautifulSoup(html, "lxml")

        # 标题（中文）
        title_cn = soup.select_one("span[property='v:itemreviewed']")
        title_cn = title_cn.get_text(strip=True) if title_cn else ""

        # 年份
        year = None
        yn = soup.select_one("#content h1 span.year")
        if yn:
            m = re.search(r"\d{4}", yn.get_text())
            year = int(m.group(0)) if m else None

        # 评分
        rating_avg = None
        ra = soup.select_one("strong[property='v:average']")
        if ra:
            try:
                rating_avg = float(ra.get_text(strip=True))
            except: pass

        rating_count = None
        rc = soup.select_one("a.rating_people span")
        if rc:
            try:
                rating_count = int(rc.get_text(strip=True).replace(",", ""))
            except: pass

        # 片长
        runtime_min = None
        rt = soup.select_one("span[property='v:runtime']")
        if rt:
            m = re.search(r"(\d+)", rt.get_text())
            runtime_min = int(m.group(1)) if m else None

        # 上映
        release_date = None
        rds = soup.select("span[property='v:initialReleaseDate']")
        if rds:
            release_date = rds[0].get_text(strip=True)

        # 海报
        poster = soup.select_one("a.nbgnbg img")
        poster_url = poster.get("src") if poster else None

        # 简介
        summary_node = soup.select_one("span[property='v:summary']")
        summary = summary_node.get_text("\n", strip=True) if summary_node else None

        return Movie(
            movie_id=self._extract_id(url),
            title_cn=title_cn,
            title_orig=None,
            year=year,
            rating_avg=rating_avg,
            rating_count=rating_count,
            runtime_min=runtime_min,
            source_url=url,
            crawl_time=datetime.utcnow(),
            release_date=release_date,
            poster_url=poster_url,
            summary=summary
        )
