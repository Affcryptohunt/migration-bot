import requests
from bs4 import BeautifulSoup
import urllib3
from urllib.parse import urljoin
# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Connection": "keep-alive"
}


def fetch_page(url):
    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10,
            verify=False
        )

        if response.status_code != 200:
            print(f"Failed to fetch page: {response.status_code}")
            return None

        return response.text

    except Exception as e:
        print(f"Error fetching page: {e}")
        return None


def parse_html(html):
    soup = BeautifulSoup(html, "lxml")
    return soup


def get_next_page(soup, base_url):

    next_button = soup.select_one("li.next a")

    if not next_button:
        return None

    href = next_button.get("href")

    next_url = urljoin(base_url, href)

    return next_url


def extract_product_links(soup, base_url=None):

    links = []

    products = soup.select("article.product_pod h3 a")

    for product in products:

        href = product.get("href")

        full_url = urljoin(base_url, href)

        links.append(full_url)

    return links
def crawl_category(category_url):

    print(f"Fetching category page: {category_url}")

    all_product_links = []

    current_url = category_url

    while current_url:

        html = fetch_page(current_url)

        if not html:
            break

        soup = parse_html(html)

        product_links = extract_product_links(soup, current_url)

        print(f"Products found on page: {len(product_links)}")

        all_product_links.extend(product_links)

        next_page = get_next_page(soup, current_url)

        if next_page:
            print(f"Next page found: {next_page}")
        else:
            print("No more pages")

        current_url = next_page

    print(f"\nTotal product links found: {len(all_product_links)}")

    return all_product_links