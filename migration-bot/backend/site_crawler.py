import requests
import time
import random
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

from backend.product_detector import is_product_page

MAX_PAGES = 2000


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}


EXCLUDED_PATHS = [
    "/cart",
    "/checkout",
    "/login",
    "/account",
    "/search",
    "/privacy",
    "/terms"
]


def is_valid_url(url, domain):
    """
    Filters URLs to keep crawler focused on relevant pages
    """

    parsed = urlparse(url)

    if parsed.netloc != domain:
        return False

    for path in EXCLUDED_PATHS:
        if path in parsed.path.lower():
            return False

    return True


def crawl_site(start_url, max_pages=100, delay_range=(1, 3)):

    session = requests.Session()
    to_visit = [(start_url, 0)]
    discovered_links = set()
    visited = set()

    domain = urlparse(start_url).netloc

    while to_visit and len(visited) < MAX_PAGES:

        url, depth = to_visit.pop(0)

        if url in visited:
            continue

        try:

            print("Crawling:", url)

            delay = random.uniform(*delay_range)
            time.sleep(delay)

            r = session.get(
                url,
                headers=HEADERS,
                timeout=10
            )

            if r.status_code != 200:
                continue

            visited.add(url)

            soup = BeautifulSoup(r.text, "html.parser")

            # Discover links
            for a in soup.find_all("a", href=True):

                link = urljoin(url, a["href"])

                if not is_valid_url(link, domain):
                    continue

                if link not in visited:

                    to_visit.append((link, depth + 1))

                discovered_links.add(link)

        except Exception:
            continue

    return list(discovered_links)