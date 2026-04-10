import csv
import re


def generate_handle(title):

    handle = title.lower()

    handle = re.sub(r'[^a-z0-9\s-]', '', handle)

    handle = re.sub(r'\s+', '-', handle)

    return handle


def export_shopify_csv(products, filename="shopify_products.csv"):

    headers = [
        "Handle",
        "Title",
        "Body (HTML)",
        "Vendor",
        "Type",
        "Tags",
        "Published",
        "Option1 Name",
        "Option1 Value",
        "Variant SKU",
        "Variant Price",
        "Image Src"
    ]

    with open(filename, "w", newline="", encoding="utf-8") as csvfile:

        writer = csv.writer(csvfile)

        writer.writerow(headers)

        for product in products:

            handle = generate_handle(product.get("title", "product"))

            variants = product.get("variants", [])

            image = product["images"][0] if product.get("images") else ""

            if not variants:

                writer.writerow([
                    handle,
                    product.get("title"),
                    product.get("description"),
                    product.get("vendor"),
                product.get("category", ""),
                    product.get("price"),
                    image
                ])

            else:

                first_variant = True

                for variant in variants:

                    writer.writerow([
                        handle,
                        product.get("title") if first_variant else "",
                        product.get("description") if first_variant else "",
                        product.get("vendor") if first_variant else "",
                        product.get("category", "") if first_variant else "",
                        "",
                        "TRUE",
                        variant.get("name"),
                        variant.get("name"),
                        "",
                        variant.get("price") or product.get("price"),
                        image if first_variant else ""
                    ])

                    first_variant = False

    print(f"\nShopify CSV exported: {filename}")