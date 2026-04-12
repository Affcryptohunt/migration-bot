from migrate import scrape_products_parallel
from analytics import analyze_products

def run_scrape_job(product_links):

    products = scrape_products_parallel(product_links)

    analytics = analyze_products(products)

    return {
        "products": products[:20],
        "count": len(products),
        "analytics": analytics
    }
