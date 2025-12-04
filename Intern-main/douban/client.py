# client.py
import time, random, logging, requests

class DoubanClient:
    def __init__(self, timeout=12, min_delay=1.5, max_delay=2.5):
        self.sess = requests.Session()
        self.sess.headers.update({
            "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/122.0 Safari/537.36"),
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
        })
        self.timeout = timeout
        self.min_delay = min_delay
        self.max_delay = max_delay

    def get(self, url: str) -> str:
        for attempt in range(3):
            try:
                resp = self.sess.get(url, timeout=self.timeout)
                if resp.status_code == 200:
                    time.sleep(random.uniform(self.min_delay, self.max_delay))
                    return resp.text
                logging.warning("GET %s status=%s", url, resp.status_code)
            except requests.RequestException as e:
                logging.warning("GET %s error=%s attempt=%d", url, e, attempt+1)
            time.sleep(random.uniform(self.min_delay, self.max_delay))
        raise RuntimeError(f"Failed GET {url}")
