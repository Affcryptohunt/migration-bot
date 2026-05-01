from backend.site_crawler import crawl_site
from backend.scraper import extract_products


def run_scrape_job(url):
    all_links = crawl_site(url, max_pages=50)

    products = []

    for link in all_links:
        items = extract_products(link)

        for item in items:
            products.append(item)

            # 🔥 STOP when enough products
            if len(products) >= 500:
                return products

    return products