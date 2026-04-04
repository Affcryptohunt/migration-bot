def is_product_page(url):
    """
    Basic heuristic to detect product pages from URLs
    """

    keywords = [
        "product",
        "item",
        "book",
        "shop",
        "p/",
        "/dp/"
    ]

    url = url.lower()

    for k in keywords:
        if k in url:
            return True

    return False