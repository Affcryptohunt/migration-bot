import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

visited = set()


def crawl_site(start_url, max_pages=100):

    to_visit = [start_url]
    discovered_links = set()

    domain = urlparse(start_url).netloc

    while to_visit and len(visited) < max_pages:

        url = to_visit.pop(0)

        if url in visited:
            continue

        try:
            print("Crawling:", url)

            r = requests.get(url, timeout=10)

            if r.status_code != 200:
                continue

            visited.add(url)

            soup = BeautifulSoup(r.text, "html.parser")

            for a in soup.find_all("a", href=True):

                link = urljoin(url, a["href"])

                parsed = urlparse(link)

                if parsed.netloc != domain:
                    continue

                if link not in visited:
                    to_visit.append(link)

                discovered_links.add(link)

        except Exception:
            continue

    return list(discovered_links)