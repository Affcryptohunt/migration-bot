import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

<<<<<<< HEAD
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

=======
>>>>>>> bc7c579 (Add product page detection module)

def find_category_links(homepage_url):

    print("Scanning homepage for category links...")

<<<<<<< HEAD
    try:
        response = requests.get(homepage_url, headers=HEADERS, timeout=10)
    except Exception:
        return []

=======
    response = requests.get(homepage_url)
>>>>>>> bc7c579 (Add product page detection module)
    soup = BeautifulSoup(response.text, "html.parser")

    category_links = set()

<<<<<<< HEAD
    keywords = [
        "category",
        "collection",
        "collections",
        "product-category",
        "shop"
    ]

    for link in soup.find_all("a", href=True):

        href = link["href"].lower()

        if any(keyword in href for keyword in keywords):

            full_url = urljoin(homepage_url, href)

            category_links.add(full_url)

    print("Categories found:", len(category_links))

=======
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

>>>>>>> bc7c579 (Add product page detection module)
    return list(category_links)