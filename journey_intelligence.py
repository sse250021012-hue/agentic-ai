from collections import Counter
import json

def get_customer_events(customer_id):

    with open("data/journey_events.json", "r") as f:
        events = json.load(f)

    return [
        e for e in events
        if e["customer_id"] == customer_id
    ]

def build_profile(customer_id):

    events = get_customer_events(customer_id)

    event_counts = Counter(
        event["event_type"]
        for event in events
    )

    channel_counts = Counter(
        event["channel"]
        for event in events
    )

    sku_counts = Counter(
        event["sku"]
        for event in events
        if event.get("sku")
    )

    preferred_channel = (
        channel_counts.most_common(1)[0][0]
        if channel_counts else "Unknown"
    )

    favorite_products = [
        sku
        for sku, count in sku_counts.most_common(3)
    ]

    purchases = event_counts["purchase"]
    cart = event_counts["cart"]
    wishlist = event_counts["wishlist"]

    if purchases > 0:
        intent = "Very High"
    elif cart > 0:
        intent = "High"
    elif wishlist > 0:
        intent = "Medium"
    else:
        intent = "Low"

    return {
        "customer_id": customer_id,
        "views": event_counts["view"],
        "wishlist": wishlist,
        "cart": cart,
        "purchase": purchases,
        "purchase_intent": intent,
        "preferred_channel": preferred_channel,
        "favorite_products": favorite_products
    }
def generate_memory(customer_id):

    profile = build_profile(customer_id)

    memory = f"""
Customer ID: {customer_id}

Preferred Channel:
{profile['preferred_channel']}

Purchase Intent:
{profile['purchase_intent']}

Frequently Viewed Products:
{', '.join(profile['favorite_products'])}
"""

    return memory
print(generate_memory("C001"))
def save_memory(customer_id):

    memory = generate_memory(customer_id)

    with open("data/customer_memories.json", "r") as f:
        memories = json.load(f)

    memories[customer_id] = memory

    with open("data/customer_memories.json", "w") as f:
        json.dump(memories, f, indent=4)

save_memory("C001")