import json
import pandas as pd

products = pd.read_csv("data/products.csv")

with open("data/journey_events.json", "r") as f:
    events = json.load(f)
from collections import Counter

customer_memories = {}

customer_ids = set(
    event["customer_id"]
    for event in events
)
for customer_id in customer_ids:

    customer_events = [
        e for e in events
        if e["customer_id"] == customer_id
    ]

    channels = [
        e["channel"]
        for e in customer_events
    ]

    preferred_channel = Counter(
        channels
    ).most_common(1)[0][0]
    categories = []

    for event in customer_events:

        sku = event["sku"]

        product = products[
            products["sku"] == sku
        ]

        if not product.empty:

            categories.append(
                product.iloc[0]["terms"]
            )

    favorite_category = "unknown"

    if categories:
        favorite_category = Counter(
            categories
        ).most_common(1)[0][0]
    event_types = [
        e["event_type"]
        for e in customer_events
    ]

    if "purchase" in event_types:
        intent = "Very High"

    elif "cart" in event_types:
        intent = "High"

    elif "wishlist" in event_types:
        intent = "Medium"

    else:
        intent = "Low"
    customer_memories[customer_id] = {
        "preferred_channel": preferred_channel,
        "favorite_category": favorite_category,
        "purchase_intent": intent
    }
with open(
    "data/customer_memories.json",
    "w"
) as f:
    json.dump(
        customer_memories,
        f,
        indent=4
    )

print(customer_memories)