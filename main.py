import os

print("Current directory:", os.getcwd())
print("Files inside data folder:")

if os.path.exists("data"):
    print(os.listdir("data"))
else:
    print("data folder not found")
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import json
import random
from datetime import datetime

app = FastAPI(
    title="Fashion Journey Intelligence Platform",
    version="1.0"
)

# =========================
# LOAD DATA
# =========================

products_df = pd.read_csv(
    "data/products.csv",
    dtype={"sku": str}
)

products_df = products_df.fillna("")
products_df["sku"] = (
    products_df["sku"]
    .astype(str)
    .str.strip()
)

print("Products loaded:", len(products_df))
print("Columns:")
print(products_df.columns.tolist())

with open("data/customers.json", "r") as f:
    customers = json.load(f)

with open("data/inventory.json", "r") as f:
    inventory = json.load(f)

with open("data/loyalty.json", "r") as f:
    loyalty = json.load(f)

with open("data/pos.json", "r") as f:
    pos_data = json.load(f)
# =========================
# REQUEST MODELS
# =========================

class PaymentRequest(BaseModel):
    customer_id: str
    amount: float


class EventRequest(BaseModel):
    customer_id: str
    event_type: str
    channel: str
    sku: str | None = None

# =========================
# PRODUCT CATALOG API
# =========================

@app.get("/")
def home():
    return {
        "message": "Fashion Journey Intelligence Platform Running"
    }


@app.get("/products")
def get_products():

    return (
        products_df
        .fillna("")
        .to_dict(orient="records")
    )


@app.get("/products/{sku}")
def get_product(sku: str):

    sku = sku.strip()

    product = products_df[
        products_df["sku"] == sku
    ]

    if product.empty:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return (
        product
        .fillna("")
        .iloc[0]
        .to_dict()
    )


@app.get("/products/search")
def search_products(
    category: str = None,
    max_price: float = None
):

    results = products_df.copy()

    if category:

        results = results[
            results["Product Category"]
            .astype(str)
            .str.contains(
                category,
                case=False,
                na=False
            )
        ]

    if max_price:

        results = results[
            results["price"] <= max_price
        ]

    return (
        results
        .fillna("")
        .to_dict(orient="records")
    )


@app.get("/skus")
def get_skus():

    return (
        products_df["sku"]
        .head(50)
        .tolist()
    )

# =========================
# CUSTOMER API
# =========================

@app.get("/customers")
def get_customers():
    return customers


@app.get("/customers/{customer_id}")
def get_customer(customer_id: str):

    for customer in customers:
        if customer["customer_id"] == customer_id:
            return customer

    raise HTTPException(
        status_code=404,
        detail="Customer not found"
    )


# =========================
# INVENTORY API
# =========================

@app.get("/inventory")
def get_inventory():
    return inventory


@app.get("/inventory/{sku}")
def get_inventory_by_sku(sku: str):

    if sku not in inventory:
        raise HTTPException(
            status_code=404,
            detail="SKU not found"
        )

    return inventory[sku]


@app.get("/inventory/{sku}/{size}")
def check_stock(
    sku: str,
    size: str
):

    if sku not in inventory:
        raise HTTPException(
            status_code=404,
            detail="SKU not found"
        )

    qty = inventory[sku]["sizes"].get(
        size.upper(),
        0
    )

    return {
        "sku": sku,
        "size": size.upper(),
        "quantity": qty,
        "available": qty > 0
    }


# =========================
# LOYALTY API
# =========================

@app.get("/loyalty")
def get_all_loyalty():
    return loyalty


@app.get("/loyalty/{customer_id}")
def get_loyalty(customer_id: str):

    if customer_id not in loyalty:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return loyalty[customer_id]


# =========================
# POS API
# =========================

@app.get("/pos")
def get_pos():
    return pos_data


@app.get("/pos/{customer_id}")
def get_customer_pos(customer_id: str):

    return pos_data.get(
        customer_id,
        []
    )


# =========================
# PAYMENT API
# =========================

@app.post("/payment")
def process_payment(
    payment: PaymentRequest
):

    status = random.choice(
        [
            "success",
            "bank_timeout",
            "upi_failure",
            "card_declined"
        ]
    )

    return {
        "customer_id": payment.customer_id,
        "amount": payment.amount,
        "status": status
    }


# =========================
# JOURNEY EVENT API
# =========================

@app.post("/journey/event")
def record_event(
    event: EventRequest
):

    try:
        with open(
            "data/journey_events.json",
            "r"
        ) as f:
            events = json.load(f)

    except:
        events = []

    new_event = {
        "customer_id": event.customer_id,
        "event_type": event.event_type,
        "channel": event.channel,
        "sku": event.sku,
        "timestamp": str(datetime.now())
    }

    events.append(new_event)

    with open(
        "data/journey_events.json",
        "w"
    ) as f:
        json.dump(
            events,
            f,
            indent=4
        )

    return {
        "message": "Event recorded",
        "event": new_event
    }


@app.get("/journey/{customer_id}")
def get_journey(
    customer_id: str
):

    try:
        with open(
            "data/journey_events.json",
            "r"
        ) as f:
            events = json.load(f)

    except:
        events = []

    customer_events = [
        event
        for event in events
        if event["customer_id"] == customer_id
    ]

    return customer_events

@app.get("/test")
def test():
    return {
        "rows": len(products_df),
        "columns": products_df.columns.tolist()
    }

