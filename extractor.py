import json
from urllib.parse import urljoin
from image_processor import download_image


def extract_json_ld_product(soup):
    """
    Extract product data from JSON-LD structured data
    """

    scripts = soup.find_all("script", type="application/ld+json")

    for script in scripts:
        try:
            data = json.loads(script.string)

            # Sometimes JSON-LD is inside a list
            if isinstance(data, list):
                for item in data:
                    product = parse_product(item)
                    if product:
                        return product

            else:
                product = parse_product(data)
                if product:
                    return product

        except Exception:
            continue

    return None


def parse_product(data):

    if not isinstance(data, dict):
        return None

    if data.get("@type") != "Product":
        return None

    product = {
        "title": data.get("name"),
        "description": data.get("description"),
        "price": None,
        "images": [],
        "sku": data.get("sku"),
        "vendor": data.get("brand", {}).get("name") if isinstance(data.get("brand"), dict) else None
    }

    # Extract images
    images = data.get("image")

    downloaded_images = []

    if isinstance(images, list):
        for img_url in images:
            saved_path = download_image(img_url)
            if saved_path:
                downloaded_images.append(saved_path)

    elif isinstance(images, str):
        saved_path = download_image(images)
        if saved_path:
            downloaded_images.append(saved_path)

    product["images"] = downloaded_images

    # Extract price
    offers = data.get("offers")

    if isinstance(offers, dict):
        product["price"] = offers.get("price")

    return product
from urllib.parse import urljoin


def extract_dom_product(soup, base_url=None):

    try:

        # Title detection
        title = None
        title_selectors = [
            "h1",
            ".product-title",
            ".product_name",
            ".product_title"
        ]

        for selector in title_selectors:
            tag = soup.select_one(selector)
            if tag:
                title = tag.text.strip()
                break

        # Price detection
        price = None
        price_selectors = [
            ".price",
            ".price_color",
            ".product-price",
            ".woocommerce-Price-amount"
        ]

        for selector in price_selectors:
            tag = soup.select_one(selector)
            if tag:
                price = tag.text.strip()
                break

        # Image detection
        images = []
        img = soup.select_one("img")

        if img:
            src = img.get("src")
            if src:
                img_url = urljoin(base_url, src)

                saved_path = download_image(img_url)

                if saved_path:
                    images.append(saved_path)

        product = {
            "title": title,
            "description": None,
            "price": price,
            "images": images,
            "sku": None,
            "vendor": None
        }

        if title:
            return product

        return None

    except Exception:
        return None