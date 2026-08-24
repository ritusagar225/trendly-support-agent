from datetime import datetime, timezone
from uuid import uuid4


def escalate_to_human(
    reason: str,
    summary: str,
    order_id: str | None = None,
) -> dict:
    """
    Create a human-support escalation record.

    This is currently an in-memory implementation.
    A production version would persist the case in a
    ticketing/CRM system.
    """

    case_id = f"CASE-{uuid4().hex[:8].upper()}"

    return {
        "status": "escalated",
        "case_id": case_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "reason": reason,
        "summary": summary,
        "order_id": order_id,
        "assigned_to": "human_support",
    }


if __name__ == "__main__":
    result = escalate_to_human(
        reason="lost_parcel",
        summary="Customer's parcel is marked lost in transit.",
        order_id="TR-4526",
    )

    print(result)