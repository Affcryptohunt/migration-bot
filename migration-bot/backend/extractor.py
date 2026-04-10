import json
from urllib.parse import urljoin


def extract_json_ld_product(soup):
    """
    Extract product data from JSON-LD structured data
    """

    scripts = soup.find_all("script", type="application/ld+json")

    for script in scripts:

        if not script.string:
            continue

        try:
            data = json.loads(script.string)
        except Exception:
            continue

        # JSON-LD can be a list
        if isinstance(data, list):

            for item in data:
                product = parse_product(item)

                if product:
                    return product

        else:

            product = parse_product(data)

            if product:
                return product

    return None


def parse_product(data):

    if not isinstance(data, dict):
        return None

    product_type = data.get("@type")

    if isinstance(product_type, list):
        product_type = " ".join(product_type)

    if not product_type or "Product" not in str(product_type):
        return None

    product = {
        "title": data.get("name"),
        "description": data.get("description"),
        "price": None,
        "currency": None,
        "images": [],
        "sku": data.get("sku"),
        "vendor": None,
        "category": data.get("category") or "",
        "variants": []
    }

    # Brand/vendor
    brand = data.get("brand")

    if isinstance(brand, dict):
        product["vendor"] = brand.get("name")

    elif isinstance(brand, str):
        product["vendor"] = brand

    # Images
    images = data.get("image")

    if isinstance(images, list):
        product["images"] = images

    elif isinstance(images, str):
        product["images"] = [images]

    # Price
    offers = data.get("offers")

    if isinstance(offers, dict):

        product["price"] = offers.get("price")
        product["currency"] = offers.get("priceCurrency")

    elif isinstance(offers, list):

        for offer in offers:

            price = offer.get("price")

            if price:
                product["price"] = price
                product["currency"] = offer.get("priceCurrency")
                break

    return product


def extract_dom_product(soup, base_url=None):
    """
    Extract product data from HTML when JSON-LD is unavailable
    """

    try:

        # TITLE
        title = None

        title_selectors = [
            "h1.product-title",
            "h1.product_title",
            "h1.product-name",
            "h1",
        ]

        for selector in title_selectors:

            tag = soup.select_one(selector)

            if tag:
                title = tag.text.strip()
                break

        if not title:
            return None

        # PRICE
        price = None

        price_selectors = [
            ".price",
            ".product-price",
            ".woocommerce-Price-amount",
            "[class*=price]"
        ]

        for selector in price_selectors:

            tag = soup.select_one(selector)

            if tag:
                price = tag.text.strip()
                break

        # CATEGORY
        category = None

        category_selectors = [
            ".product-category",
            ".product-category a",
            ".category",
            ".breadcrumb .category"
        ]

        for selector in category_selectors:

            tag = soup.select_one(selector)

            if tag:
                category = tag.text.strip()
                break

        # DESCRIPTION
        description = None

        description_selectors = [
            ".product-description",
            ".woocommerce-product-details__short-description",
            "#description",
            "[class*=description]"
        ]

        for selector in description_selectors:

            tag = soup.select_one(selector)

            if tag:
                description = tag.text.strip()
                break

        # IMAGES
        images = []

        image_selectors = [
            ".product-gallery img",
            ".product-image img",
            ".woocommerce-product-gallery img",
            "img[src*='product']"
        ]

        for selector in image_selectors:

            tags = soup.select(selector)

            for img in tags:

                src = img.get("src") or img.get("data-src")

                if src:

                    img_url = urljoin(base_url, src)

                    if img_url not in images:
                        images.append(img_url)

            if images:
                break

        # VARIANTS
        variants = extract_variants(soup, price)

        product = {
            "title": title,
            "description": description,
            "price": price,
            "currency": None,
            "images": images,
            "sku": None,
            "vendor": None,
            "category": category or "",
            "variants": variants
        }

        return product

    except Exception:

        return None


def extract_variants(soup, price=None):

    variants = []

    for option in soup.select("select option"):

        value = option.text.strip()

        if not value:
            continue

        if "choose" in value.lower():
            continue

        variants.append({
            "name": value,
            "price": price,
        })

    return variants