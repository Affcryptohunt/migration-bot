import csv
import re

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def export_shopify_csv(products, filename="shopify_products.csv"):
    
    fields = [
        "Handle",
        "Title",
        "Body (HTML)",
        "Vendor",
        "Type",
        "Tags",
        "Published",
        "Variant Price",
        "Image Src"
    ]

    rows = []

    for product in products:
        title = product.get("title", "")
        handle = slugify(title)

        row = {
            "Handle": handle,
            "Title": title,
            "Body (HTML)": product.get("description", ""),
            "Vendor": product.get("vendor", "Imported"),
            "Type": product.get("type", ""),
            "Tags": "",
            "Published": "TRUE",
            "Variant Price": product.get("price", ""),
            "Image Src": product.get("image", "")
        }

        rows.append(row)

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Shopify CSV exported: {filename}")