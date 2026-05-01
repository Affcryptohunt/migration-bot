import requests
from bs4 import BeautifulSoup


def run_scrape_job(url):
    products = []
    page = 1

    while len(products) < 500:
        page_url = f"{url}/catalogue/page-{page}.html" if page > 1 else url

        print("Scraping:", page_url)

        res = requests.get(page_url)
        if res.status_code != 200:
            break

        soup = BeautifulSoup(res.text, "html.parser")

        items = soup.select(".product_pod")

        if not items:
            break

        for item in items:
            name = item.h3.a["title"]
            price = item.select_one(".price_color").text

            products.append({
                "name": name,
                "price": price
            })

            if len(products) >= 500:
                break

        page += 1

    return products