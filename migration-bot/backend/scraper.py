from backend.migrate import scrape_product


def extract_products(link):
    """
    Extract products from a single link.
    Returns a list of products (0 or 1 item).
    """
    try:
        product = scrape_product(link)
        if product:
            return [product]
        return []
    except Exception as e:
        print(f"Error extracting from {link}: {e}")
        return []
