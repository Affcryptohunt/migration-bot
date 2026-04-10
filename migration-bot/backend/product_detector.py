from urllib.parse import urlparse

BAD_PATTERNS = [
    "/cart",
    "/account",
    "/login",
    "/search",
    "/policy",
    "/blog"
]


def is_product_page(url, soup=None):
    """
    Detect product pages using URL patterns and page metadata
    """

    url = url.lower()

    parsed = urlparse(url)

    path = parsed.path

    for bad in BAD_PATTERNS:
        if bad in url:
            return False

    # obvious non-product pages
    blacklist = [
        "cart",
        "checkout",
        "account",
        "login",
        "register",
        "privacy",
        "terms",
        "about",
        "contact",
        "blog",
        "news"
    ]

    for word in blacklist:
        if word in path:
            return False

    # strong product indicators
    product_keywords = [
        "/product",
        "/products/",
        "/item/",
        "/p/",
        "/dp/",
        "/catalogue/"
    ]

    for keyword in product_keywords:
        if keyword in path:
            return True

    # weaker indicators
    weak_keywords = [
        "/shop/",
        "/store/",
        "/buy/"
    ]

    for keyword in weak_keywords:
        if keyword in path:
            return True

    # Content detection (if soup provided)
    if soup:

        # JSON-LD product schema
        scripts = soup.select("script[type='application/ld+json']")

        for script in scripts:

            if script.string and "product" in script.string.lower():
                return True

        # OpenGraph metadata
        og = soup.select_one("meta[property='og:type']")

        if og:

            content = og.get("content", "").lower()

            if "product" in content:
                return True

        # price metadata
        price_meta = soup.select_one("meta[property*='price'], meta[name*='price']")

        if price_meta:
            return True

    return False