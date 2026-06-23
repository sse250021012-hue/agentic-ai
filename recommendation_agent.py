import pandas as pd
import json

products = pd.read_csv("data/products.csv")
products["price_inr"] = (
    products["price"] * 95
).round()

with open("data/inventory.json", "r") as f:
    inventory = json.load(f)

print(products[["sku", "price", "price_inr"]].head())

def recommend_products(category, budget):

    results = products[
        (
            products["terms"]
            .str.contains(
                category,
                case=False,
                na=False
            )
        )
        &
        (
            products["price_inr"] <= budget
        )
    ]

    recommendations = []

    for _, row in results.iterrows():

        sku = row["sku"]

        if sku in inventory:

            stock = inventory[sku]["sizes"]

            total_stock = sum(stock.values())

            if total_stock > 0:

                recommendations.append(
                    {
                        "sku": sku,
                        "name": row["name"],
                        "price_usd": row["price"],
                        "price_inr": row["price_inr"],
                        "stock": total_stock
                    }
                )
                print("Category:", category)
                print("Budget:", budget)

    return recommendations[:5]

print(products["terms"].unique())
print(
    recommend_products(
        "jeans",
        7000
    )
)
