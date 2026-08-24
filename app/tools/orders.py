import json
from pathlib import Path


DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "orders.json"


def load_orders() -> dict:
    """Load the fixed Trendly order dataset without modifying it."""
    with open(DATA_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def get_order(order_id: str) -> dict | None:
    """
    Look up an order by order ID.

    Returns the order if found, otherwise None.
    """
    data = load_orders()

    for order in data["orders"]:
        if order["order_id"].upper() == order_id.upper():
            return order

    return None


