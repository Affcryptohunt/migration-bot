import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

from platform_detector import detect_platform
from site_crawler import crawl_site
from product_detector import is_product_page
from extractor import extract_json_ld_product, extract_dom_product
from image_processor import download_image
from csv_exporter import export_shopify_csv
from analytics import analyze_products

import requests
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

MAX_WORKERS = 10
MAX_PRODUCTS = 500


def fetch_page(url):

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=15
        )

        if response.status_code == 200:
            return response.text

    except Exception as e:
        print("Request error:", e)

    return None


def parse_html(html):

    return BeautifulSoup(html, "lxml")


def scrape_product(url):

    html = fetch_page(url)

    if not html:
        return None

    soup = parse_html(html)

    product = extract_json_ld_product(soup)

    if not product:
        product = extract_dom_product(soup, url)

    if not product:
        return None

    print("Product extracted:", product["title"])

    # download images
    images = product.get("images", [])

    downloaded = []

    for img in images:

        saved = download_image(img)

        if saved:
            downloaded.append(saved)

    product["images"] = downloaded

    return product


def main():

    if len(sys.argv) < 2:
        print("Usage: python migrate.py <store_url>")
        return

    url = sys.argv[1]

    print("\nDetecting platform...")

    platform = detect_platform(url)

    print("Platform detected:", platform)

    print("\nCrawling site...")

    all_links = crawl_site(url)

    print("Total links discovered:", len(all_links))

    product_links = []

    for link in all_links:

        if is_product_page(link):
            product_links.append(link)

    product_links = list(set(product_links))

    print("Detected product pages:", len(product_links))

    if len(product_links) > MAX_PRODUCTS:
        product_links = product_links[:MAX_PRODUCTS]

    print("\nScraping products in parallel...")

    all_products = scrape_products_parallel(product_links)

    print("\nTotal products extracted:", len(all_products))

    if all_products:

        export_shopify_csv(all_products)

    else:

        print("No products extracted.")


def scrape_products_parallel(product_links):

    products = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:

        futures = {
            executor.submit(scrape_product, link): link
            for link in product_links[:MAX_PRODUCTS]
        }

        for future in as_completed(futures):

            try:
                product = future.result()

                if product:
                    products.append(product)

            except Exception as e:
                print("Scrape error:", e)

    return products


def run_migration(url):

    platform = detect_platform(url)

    links = crawl_site(url)

    product_links = list({link for link in links if is_product_page(link)})

    products = scrape_products_parallel(product_links)

    filename = f"storage/exports/products.csv"

    export_shopify_csv(products, filename)

    analytics = analyze_products(products)

    return {
        "platform": platform,
        "product_count": len(products),
        "products": products[:20],  # preview only
        "analytics": analytics,
        "csv_file": filename
    }


if __name__ == "__main__":
    main()