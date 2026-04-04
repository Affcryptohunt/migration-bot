import csv


def export_shopify_csv(products, filename="products.csv"):

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:

        writer = csv.writer(csvfile)

        for product in products:

            variants = product.get("variants", [])

            if not variants:
                writer.writerow([
                    product["title"],
                    product["price"],
                    product["images"][0] if product["images"] else ""
                ])
            else:
                for variant in variants:
                    writer.writerow([
                        product["title"],
                        variant["price"] or product["price"],
                        product["images"][0] if product["images"] else ""
                    ])

    print(f"\nCSV exported: {filename}")