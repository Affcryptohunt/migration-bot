import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from platform_detector import detect_platform
from crawler import crawl_category, fetch_page, parse_html
from extractor import extract_json_ld_product, extract_dom_product
from csv_exporter import export_shopify_csv
from category_finder import find_category_links
from site_crawler import crawl_site
from product_detector import is_product_page

def scrape_product(url):

    html = fetch_page(url)

    if not html:
        return None

    soup = parse_html(html)

    product = extract_json_ld_product(soup)

    if not product:
        product = extract_dom_product(soup, url)

    if product:
        print("Product extracted:", product["title"])

    return product


def get_product_links(category_url):

    product_links = crawl_category(category_url)

    return product_links


def main():

    if len(sys.argv) < 2:
        print("Usage: python migrate.py <url>")
        return

    url = sys.argv[1]

    print("\nScanning site...")

    platform = detect_platform(url)

    print("Platform detected:", platform)

    print("Discovering site pages...")

    all_links = crawl_site(url)

    print("Total links discovered:", len(all_links))

    product_links = []

    for link in all_links:

        if is_product_page(link):
            product_links.append(link)

    print("Detected product pages:", len(product_links))

    all_products = []

    print("Scraping products in parallel...")

    with ThreadPoolExecutor(max_workers=8) as executor:

        futures = [executor.submit(scrape_product, link) for link in product_links]

        for future in as_completed(futures):

            product = future.result()

            if product:
                all_products.append(product)

    print("\nTotal products extracted:", len(all_products))

    if all_products:
        export_shopify_csv(all_products)


if __name__ == "__main__":
    main()