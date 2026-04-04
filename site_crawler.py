import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


visited = set()


def crawl_site(start_url, max_pages=500):

    to_visit = [start_url]
    discovered_links = []

    domain = urlparse(start_url).netloc

    while to_visit and len(visited) < max_pages:

        url = to_visit.pop(0)

        if url in visited:
            continue

        try:
            print("Crawling:", url)

            res = requests.get(url, timeout=10)

            visited.add(url)

            soup = BeautifulSoup(res.text, "html.parser")

            for link in soup.find_all("a", href=True):

                href = link["href"]

                absolute = urljoin(url, href)

                parsed = urlparse(absolute)

                if parsed.netloc != domain:
                    continue

                if absolute not in visited:
                    to_visit.append(absolute)

                discovered_links.append(absolute)

        except Exception:
            continue

    return list(set(discovered_links))