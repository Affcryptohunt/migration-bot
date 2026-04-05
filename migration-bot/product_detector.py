def is_product_page(url):
    """
    Very simple heuristic to detect product pages from URL patterns
    """

    url = url.lower()

    product_keywords = [
        "/product",
        "/item",
        "/book",
        "/p/",
        "/dp/",
        "/catalogue/"
    ]

    for keyword in product_keywords:
        if keyword in url:
            return True

    return False