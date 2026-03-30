import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

from crawler import fetch_page, parse_html, extract_product_links
from extractor import extract_json_ld_product, extract_dom_product
from csv_exporter import export_shopify_csv
from category_finder import find_category_links


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

    html = fetch_page(category_url)

    if not html:
        return []

    soup = parse_html(html)

    links = extract_product_links(soup, category_url)

    return links


def main():

    if len(sys.argv) < 2:
        print("Usage: python migrate.py <url>")
        return

    url = sys.argv[1]

    if "category" in url or "catalog" in url:
        category_urls = [url]
    else:
        category_urls = find_category_links(url)

    all_products = []

    for category_url in category_urls:

        print("\nProcessing category:", category_url)

        product_links = get_product_links(category_url)

        print(f"Found {len(product_links)} products")

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