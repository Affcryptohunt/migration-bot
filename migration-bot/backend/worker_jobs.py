def run_scrape_job(url):
    from backend.site_crawler import crawl_site
    from backend.product_detector import is_product_page
    from backend.migrate import scrape_products_parallel, analyze_products
    from backend.platform_detector import detect_platform
    
    platform = detect_platform(url)
    links = crawl_site(url, max_pages=20)
    product_links = list({link for link in links if is_product_page(link)})
    products = scrape_products_parallel(product_links)
    analytics = analyze_products(products)
    
    return {
        "products": products[:20],
        "count": len(products),
        "platform": platform,
        "analytics": analytics
    }