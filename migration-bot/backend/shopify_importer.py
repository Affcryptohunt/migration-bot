import requests


def import_products_to_shopify(products, shop, token):

    url = f"https://{shop}/admin/api/2024-01/products.json"

    headers = {
        "X-Shopify-Access-Token": token,
        "Content-Type": "application/json"
    }

    created = 0

    for p in products:

        payload = {
            "product": {
                "title": p["title"],
                "body_html": p.get("description", ""),
                "variants": [
                    {
                        "price": p["price"]
                    }
                ],
                "images": [
                    {"src": img} for img in p.get("images", [])
                ]
            }
        }

        try:

            r = requests.post(url, json=payload, headers=headers)

            if r.status_code == 201:
                created += 1

        except Exception:
            pass

    return created
