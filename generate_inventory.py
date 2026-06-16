import pandas as pd
import json
import random

products = pd.read_csv("data/products.csv")

inventory = {}

for _, row in products.iterrows():

    inventory[row["sku"]] = {
        "sku": row["sku"],
        "sizes": {
            "XS": random.randint(0, 25),
            "S": random.randint(0, 25),
            "M": random.randint(0, 25),
            "L": random.randint(0, 25),
            "XL": random.randint(0, 25)
        }
    }

with open("data/inventory.json", "w") as f:
    json.dump(inventory, f, indent=4)

print("Inventory generated successfully!")