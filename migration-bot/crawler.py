import requests
from bs4 import BeautifulSoup
import urllib3
from urllib.parse import urljoin
import time
import random

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}


def fetch_page(url, retries=3):

    for attempt in range(retries):

        try:

            delay = random.uniform(1, 3)
            time.sleep(delay)

            response = requests.get(
                url,
                headers=HEADERS,
                timeout=10,
                verify=False
            )

            if response.status_code == 200:
                return response.text

            print(f"Status code: {response.status_code}")

        except Exception as e:
            print("Request error:", e)

        time.sleep(2)

    print("Failed to fetch:", url)

    return None


def parse_html(html):

    soup = BeautifulSoup(html, "lxml")

    return soup


def get_next_page(soup, base_url):

    next_button = soup.select_one("li.next a")

    if not next_button:
        return None

    href = next_button.get("href")

    return urljoin(base_url, href)


def extract_product_links(soup, base_url):

    links = []

    products = soup.select("article.product_pod h3 a")

    for product in products:

        href = product.get("href")

        full_url = urljoin(base_url, href)

        links.append(full_url)

    return links


def crawl_category(category_url):

    print("Crawling category:", category_url)

    product_links = []

    current_url = category_url

    while current_url:

        html = fetch_page(current_url)

        if not html:
            break

        soup = parse_html(html)

        links = extract_product_links(soup, current_url)

        product_links.extend(links)

        next_page = get_next_page(soup, current_url)

        if not next_page:
            break

        current_url = next_page

    return list(set(product_links))