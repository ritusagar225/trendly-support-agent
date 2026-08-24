from datetime import datetime, date

from .orders import get_order


def _parse_date(value: str) -> date:
    """Convert an ISO timestamp/date into a date."""
    return datetime.fromisoformat(
        value.replace("Z", "+00:00")
    ).date()


def check_exchange_eligibility(
    order_id: str,
    requested_size: str,
    current_date: str,
    exchange_count: int = 0,
    available_sizes: list[str] | None = None,
) -> dict:
    """
    Determine whether an item is eligible for a size exchange.

    Policy rules:
    - Size exchanges only.
    - Same 30-day window as returns.
    - One exchange per item.
    - Second exchange requires human approval.
    - If requested size is unavailable, exchange becomes a refund.
    """

    order = get_order(order_id)

    if order is None:
        return {
            "eligible": False,
            "action": "not_found",
            "reason": f"Order {order_id} was not found.",
        }

    if order["status"] == "cancelled":
        return {
            "eligible": False,
            "action": "no_exchange",
            "reason": "Cancelled orders cannot have an exchange raised.",
            "order_id": order_id,
        }

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

    if order["delivered_at"] is None:
        return {
            "eligible": False,
            "action": "not_eligible",
            "reason": "An exchange can only be requested after delivery.",
            "order_id": order_id,
        }

    delivered_date = _parse_date(order["delivered_at"])
    requested_date = _parse_date(current_date)

    days_since_delivery = (
        requested_date - delivered_date
    ).days

    if days_since_delivery < 0:
        return {
            "eligible": False,
            "action": "invalid_date",
            "reason": (
                "The supplied current date is before "
                "the delivery date."
            ),
            "order_id": order_id,
        }

    if days_since_delivery > 30:
        return {
            "eligible": False,
            "action": "not_eligible",
            "reason": (
                "The 30-calendar-day exchange window has expired."
            ),
            "order_id": order_id,
            "delivered_date": str(delivered_date),
            "days_since_delivery": days_since_delivery,
        }

    # Trendly supports size exchanges only.
    requested_size = requested_size.strip()

    if not requested_size:
        return {
            "eligible": False,
            "action": "clarification_needed",
            "reason": "A requested size is required for a size exchange.",
            "order_id": order_id,
        }

    # One exchange per item. A second requires human approval.
    if exchange_count >= 1:
        return {
            "eligible": False,
            "action": "escalate",
            "reason": (
                "A second exchange request for the same item "
                "requires human approval."
            ),
            "order_id": order_id,
        }

    # If availability data is supplied, verify the requested size.
    if available_sizes is not None:
        normalised_sizes = {
            str(size).strip().lower()
            for size in available_sizes
        }

        if requested_size.lower() not in normalised_sizes:
            return {
                "eligible": False,
                "action": "refund",
                "reason": (
                    f"Requested size {requested_size} is unavailable. "
                    "The exchange should be converted to a refund."
                ),
                "order_id": order_id,
                "requested_size": requested_size,
            }

    return {
        "eligible": True,
        "action": "exchange_eligible",
        "reason": (
            "The order is within the 30-day exchange window "
            "and is eligible for a size exchange."
        ),
        "order_id": order_id,
        "requested_size": requested_size,
        "delivered_date": str(delivered_date),
        "days_since_delivery": days_since_delivery,
    }




