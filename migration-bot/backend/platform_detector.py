import requests


HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def detect_platform(url):

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10
        )

        html = response.text.lower()

        headers_text = str(response.headers).lower()

    except Exception:
        return "unknown"

    # Shopify detection
    if (
        "cdn.shopify.com" in html
        or "shopify.theme" in html
        or "x-shopify-stage" in headers_text
        or "myshopify.com" in html
    ):
        return "shopify"

    # WooCommerce detection
    if (
        "woocommerce" in html
        or "wp-content/plugins/woocommerce" in html
        or "wp-json/wc" in html
    ):
        return "woocommerce"

    # Magento detection
    if (
        "mage/cookies.js" in html
        or "magento" in html
        or "mage-" in html
    ):
        return "magento"

    # BigCommerce detection
    if (
        "cdn.bcapp" in html
        or "bigcommerce" in html
        or "stencil-utils" in html
    ):
        return "bigcommerce"

    return "custom"