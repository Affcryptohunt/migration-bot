def analyze_products(products):

    total_products = len(products)

    prices = []

    categories = {}

    for product in products:

        price = product.get("price")

        try:
            prices.append(float(price))
        except:
            pass

        category = product.get("category")

        if category:
            categories[category] = categories.get(category, 0) + 1

    avg_price = sum(prices) / len(prices) if prices else 0

    return {
        "total_products": total_products,
        "avg_price": round(avg_price, 2),
        "min_price": min(prices) if prices else 0,
        "max_price": max(prices) if prices else 0,
        "categories": categories
    }
