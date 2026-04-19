import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend.site_crawler import crawl_site
from backend.product_detector import is_product_page
from backend.migrate import scrape_product

def run_scrape_job(url):
    print("JOB STARTED:", url)

    try:
        all_links = crawl_site(url)
        print("Links found:", len(all_links))

        product_links = [l for l in all_links if is_product_page(l)]
        print("Product links:", len(product_links))

        products = []

        for link in product_links:
            p = scrape_product(link)
            if p:
                products.append(p)

        print("Products extracted:", len(products))

        return {
            "count": len(products),
            "products": products[:50]
        }

    except Exception as e:
        print("JOB FAILED:", str(e))
        raise e
