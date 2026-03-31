import requests


HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def detect_platform(url):

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        html = response.text.lower()

    except Exception:
        return "unknown"

    # Shopify detection
    if "cdn.shopify.com" in html or "shopify.theme" in html:
        return "shopify"

    # WooCommerce detection
    if "woocommerce" in html or "wp-content/plugins/woocommerce" in html:
        return "woocommerce"

    # Magento detection
    if "mage/cookies.js" in html or "magento" in html:
        return "magento"

    # BigCommerce detection
    if "cdn.bcapp" in html or "bigcommerce" in html:
        return "bigcommerce"

    return "custom"