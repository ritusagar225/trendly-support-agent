from datetime import datetime, date
from .orders import get_order


NON_RETURNABLE_CATEGORIES = {
    "innerwear",
    "socks",
    "jewellery",
    "beauty",
    "fragrance",
    "face masks",
    "gift cards",
}


def _parse_date(value: str) -> date:
    """Convert an ISO timestamp/date into a date."""
    return datetime.fromisoformat(
        value.replace("Z", "+00:00")
    ).date()


def check_return_eligibility(
    order_id: str,
    current_date: str,
) -> dict:
    """
    Determine whether an order is eligible for a standard return.

    Business rules come from the provided Trendly policy and
    fixed orders dataset.
    """

    order = get_order(order_id)

    if order is None:
        return {
            "eligible": False,
            "action": "not_found",
            "reason": f"Order {order_id} was not found.",
        }

    # Rule 1: Cancelled orders cannot be returned.
    if order["status"] == "cancelled":
        return {
            "eligible": False,
            "action": "no_return",
            "reason": "Cancelled orders cannot have a return raised.",
            "order_id": order_id,
        }

    # Rule 2: Lost parcels are not returns.
    if order["status"] == "lost_in_transit":
        return {
            "eligible": False,
            "action": "escalate",
            "reason": (
                "This order is marked as lost in transit. "
                "It must be handled as a lost-parcel claim by a human agent."
            ),
            "order_id": order_id,
        }

    # Rule 3: A return requires delivery.
    if order["delivered_at"] is None:
        return {
            "eligible": False,
            "action": "not_eligible",
            "reason": (
                "The order has not been delivered, so the "
                "30-day return window has not started."
            ),
            "order_id": order_id,
        }

    delivered_date = _parse_date(order["delivered_at"])
    requested_date = _parse_date(current_date)

    days_since_delivery = (
        requested_date - delivered_date
    ).days

    # Rule 4: Return window is 30 calendar days from delivery.
    if days_since_delivery > 30:
        return {
            "eligible": False,
            "action": "not_eligible",
            "reason": (
                "The 30-calendar-day return window has expired."
            ),
            "order_id": order_id,
            "delivered_date": str(delivered_date),
            "days_since_delivery": days_since_delivery,
        }

    # Rule 5: Guard against an invalid date.
    if days_since_delivery < 0:
        return {
            "eligible": False,
            "action": "invalid_date",
            "reason": (
                "The supplied current date is before the "
                "order's delivery date."
            ),
            "order_id": order_id,
        }

    # Check each item in the order.
    for item in order["items"]:

        category = item.get("category", "").lower()
        final_sale = item.get("final_sale", False)

        # Rule 6: Non-returnable categories cannot be returned.
        if category in NON_RETURNABLE_CATEGORIES:
            return {
                "eligible": False,
                "action": "not_eligible",
                "reason": (
                    f"{item['name']} belongs to a non-returnable "
                    f"category: {category}."
                ),
                "order_id": order_id,
                "item": item["name"],
            }

        # Rule 7: Final-sale items are exchange-only.
        if final_sale:
            return {
                "eligible": False,
                "action": "exchange_only",
                "reason": (
                    f"{item['name']} is marked final sale. "
                    "It is eligible for size exchange only, "
                    "not a refund or store credit."
                ),
                "order_id": order_id,
                "item": item["name"],
            }

    # All standard eligibility checks passed.
    return {
        "eligible": True,
        "action": "return_eligible",
        "reason": (
            "The order is within the 30-day return window "
            "and contains returnable, non-final-sale items."
        ),
        "order_id": order_id,
        "delivered_date": str(delivered_date),
        "days_since_delivery": days_since_delivery,
    }



