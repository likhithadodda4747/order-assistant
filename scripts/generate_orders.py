"""Generate synthetic orders for the Order Assistant.

Run:  uv run scripts/generate_orders.py
Out:  data/orders.json  (200 orders, reproducible thanks to the fixed seed)
"""
import json
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

random.seed(42)  # same "random" data on every run -> reproducible evals

NUM_ORDERS = 200
OUT_PATH = Path(__file__).resolve().parent.parent / "data" / "orders.json"

CATALOG = [
    {"item_id": "SKU-10023", "name": "PS5 Console", "price": 499.00},
    {"item_id": "SKU-10024", "name": "AirPods Pro", "price": 249.00},
    {"item_id": "SKU-10025", "name": "55in 4K TV", "price": 378.00},
    {"item_id": "SKU-10026", "name": "Nintendo Switch", "price": 299.00},
    {"item_id": "SKU-10027", "name": "iPad 10th Gen", "price": 349.00},
    {"item_id": "SKU-10028", "name": "Bluetooth Speaker", "price": 59.98},
    {"item_id": "SKU-10029", "name": "Laptop 15in", "price": 549.00},
    {"item_id": "SKU-10030", "name": "Air Fryer", "price": 79.00},
    {"item_id": "SKU-10031", "name": "Coffee Maker", "price": 44.97},
    {"item_id": "SKU-10032", "name": "Vacuum Cleaner", "price": 129.00},
    {"item_id": "SKU-10033", "name": "Microwave", "price": 98.00},
    {"item_id": "SKU-10034", "name": "Office Chair", "price": 119.00},
    {"item_id": "SKU-10035", "name": "Bookshelf", "price": 64.99},
    {"item_id": "SKU-10036", "name": "Queen Bed Sheets", "price": 29.97},
    {"item_id": "SKU-10037", "name": "Bath Towel Set", "price": 24.88},
    {"item_id": "SKU-10038", "name": "Men's Jacket", "price": 39.99},
    {"item_id": "SKU-10039", "name": "Women's Sneakers", "price": 49.00},
    {"item_id": "SKU-10040", "name": "Kids' Backpack", "price": 19.97},
    {"item_id": "SKU-10041", "name": "LEGO Set", "price": 59.99},
    {"item_id": "SKU-10042", "name": "Board Game", "price": 24.99},
    {"item_id": "SKU-10043", "name": "Paper Towels 12pk", "price": 21.48},
    {"item_id": "SKU-10044", "name": "Laundry Detergent", "price": 13.97},
    {"item_id": "SKU-10045", "name": "Ground Coffee 2lb", "price": 15.48},
    {"item_id": "SKU-10046", "name": "Protein Bars 12ct", "price": 17.98},
    {"item_id": "SKU-10047", "name": "Dog Food 30lb", "price": 42.98},
    {"item_id": "SKU-10048", "name": "Cat Litter", "price": 16.47},
    {"item_id": "SKU-10049", "name": "Vitamins 100ct", "price": 11.88},
    {"item_id": "SKU-10050", "name": "Tool Kit", "price": 34.97},
    {"item_id": "SKU-10051", "name": "Garden Hose", "price": 22.97},
    {"item_id": "SKU-10052", "name": "Camping Tent", "price": 89.00},
]
STORES = ["TX-0412", "TX-0587", "CA-1180", "CA-1201", "WA-0233", "WA-0311", "NY-0901", "NY-0955"]
WAREHOUSES = [f"WH-{i:02d}" for i in range(1, 11)]
CUSTOMERS = [f"C{1000 + i}" for i in range(40)]
STATUSES = ["DELIVERED", "SHIPPED", "PROCESSING", "PAYMENT_PENDING", "CANCELLED"]
STATUS_WEIGHTS = [50, 20, 15, 10, 5]
ERRORS = ["ERR_PAY_401", "ERR_PAY_402", "ERR_PAY_403", "ERR_INV_101"]

NOW = datetime(2026, 11, 1, 12, 0, tzinfo=timezone.utc)  # fixed "today" so data doesn't drift


def iso(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def make_items(n_min: int = 1, n_max: int = 4) -> list[dict]:
    """1-4 distinct products; ~10% out of stock."""
    products = random.sample(CATALOG, random.randint(n_min, n_max))
    return [
        {
            **p,
            "qty": random.choice([1, 1, 1, 2, 3]),
            "warehouse_id": random.choice(WAREHOUSES),
            "in_stock": random.random() > 0.10,
        }
        for p in products
    ]


def make_order(order_id: str) -> dict:
    status = random.choices(STATUSES, weights=STATUS_WEIGHTS)[0]
    last_error, retries = None, 0
    if status == "PAYMENT_PENDING" and random.random() < 0.5:
        last_error = random.choice(ERRORS)
        retries = random.randint(1, 3)
    created = NOW - timedelta(days=random.randint(0, 30), minutes=random.randint(0, 1439))
    return {
        "order_id": order_id,
        "customer_id": random.choice(CUSTOMERS),
        "store_id": random.choice(STORES),
        "status": status,
        "last_error": last_error,
        "retries": retries,
        "created_at": iso(created),
        "items": make_items(),
    }


def planted_orders() -> list[dict]:
    """Hand-made orders with known answers, used in the golden set."""
    ps5 = {**CATALOG[0], "qty": 1, "warehouse_id": "WH-07", "in_stock": True}
    pods = {**CATALOG[1], "qty": 1, "warehouse_id": "WH-03", "in_stock": False}
    o1 = {  # "Did 48213 ship? If not, which items are out of stock?"
        "order_id": "48213", "customer_id": "C1007", "store_id": "TX-0412",
        "status": "PAYMENT_PENDING", "last_error": "ERR_PAY_402", "retries": 3,
        "created_at": iso(NOW - timedelta(days=2, hours=3)),
        "items": [ps5, pods],
    }
    o2 = {  # a clean delivered order with 4 items
        "order_id": "51007", "customer_id": "C1012", "store_id": "CA-1180",
        "status": "DELIVERED", "last_error": None, "retries": 0,
        "created_at": iso(NOW - timedelta(days=12)),
        "items": [{**CATALOG[i], "qty": 1, "warehouse_id": "WH-02", "in_stock": True} for i in (2, 7, 20, 23)],
    }
    o3 = {  # shipped, nothing wrong
        "order_id": "60450", "customer_id": "C1007", "store_id": "TX-0412",
        "status": "SHIPPED", "last_error": None, "retries": 0,
        "created_at": iso(NOW - timedelta(days=4)),
        "items": [{**CATALOG[5], "qty": 2, "warehouse_id": "WH-05", "in_stock": True}],
    }
    o4 = {  # inventory error (different from payment)
        "order_id": "72291", "customer_id": "C1025", "store_id": "WA-0233",
        "status": "PAYMENT_PENDING", "last_error": "ERR_INV_101", "retries": 1,
        "created_at": iso(NOW - timedelta(days=1)),
        "items": [{**CATALOG[8], "qty": 1, "warehouse_id": "WH-09", "in_stock": False}],
    }
    return [o1, o2, o3, o4]


def main() -> None:
    orders = planted_orders()
    used_ids = {o["order_id"] for o in orders}
    while len(orders) < NUM_ORDERS:
        oid = str(random.randint(10000, 99999))
        if oid in used_ids:
            continue
        used_ids.add(oid)
        orders.append(make_order(oid))

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(orders, indent=2))

    counts = {s: sum(o["status"] == s for o in orders) for s in STATUSES}
    print(f"Wrote {len(orders)} orders to {OUT_PATH}")
    print("Status counts:", counts)
    print("Orders with errors:", sum(o["last_error"] is not None for o in orders))


if __name__ == "__main__":
    main()
