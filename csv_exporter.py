import pandas as pd


def export_shopify_csv(products, filename="products.csv"):

    rows = []

    for product in products:

        row = {
            "Handle": product["title"].lower().replace(" ", "-"),
            "Title": product["title"],
            "Body (HTML)": product["description"] or "",
            "Vendor": product["vendor"] or "",
            "Variant Price": product["price"],
            "Image Src": product["images"][0] if product["images"] else ""
        }

        rows.append(row)

    df = pd.DataFrame(rows)

    df.to_csv(filename, index=False)

    print(f"\nCSV exported: {filename}")