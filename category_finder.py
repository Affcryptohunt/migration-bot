import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def find_category_links(homepage_url):
    print("Scanning homepage for category links...")

    response = requests.get(homepage_url)
    soup = BeautifulSoup(response.text, "html.parser")

    category_links = set()

    for link in soup.find_all("a", href=True):
        href = link["href"]

        keywords = [
            "category",
            "shop",
            "collection",
            "product-category"
        ]

        if any(keyword in href.lower() for keyword in keywords):
            full_url = urljoin(homepage_url, href)
            category_links.add(full_url)

    return list(category_links)
