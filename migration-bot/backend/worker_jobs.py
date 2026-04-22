def run_scrape_job(url):
    from backend.site_crawler import crawl_site
    from backend.product_detector import is_product_page
    from backend.migrate import scrape_product
    from concurrent.futures import ThreadPoolExecutor, as_completed

    try:
        # LIMIT crawling (THIS IS THE FIX)
        all_links = crawl_site(url)[:50]

        product_links = [l for l in all_links if is_product_page(l)][:20]

        products = []

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(scrape_product, link) for link in product_links]

            for future in as_completed(futures, timeout=30):  # prevent infinite wait
                try:
                    p = future.result(timeout=5)
                    if p:
                        products.append(p)
                except:
                    continue

        return {
            "products": products,
            "count": len(products)
        }

    except Exception as e:
        return {
            "error": str(e)
        }