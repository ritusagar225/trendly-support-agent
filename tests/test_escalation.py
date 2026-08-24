from app.tools.escalation import escalate_to_human


def test_lost_parcel_escalation():
    result = escalate_to_human(
        reason="lost_parcel",
        summary="Customer's parcel is marked lost in transit.",
        order_id="TR-4526",
    )

    assert result["status"] == "escalated"
    assert result["reason"] == "lost_parcel"
    assert result["order_id"] == "TR-4526"
    assert result["assigned_to"] == "human_support"
    assert result["case_id"].startswith("CASE-")


def test_escalation_without_order():
    result = escalate_to_human(
        reason="policy_not_covered",
        summary="Customer asked about a birthday discount.",
    )

    assert result["status"] == "escalated"
    assert result["reason"] == "policy_not_covered"
    assert result["order_id"] is None
    assert result["assigned_to"] == "human_support"
    assert result["case_id"].startswith("CASE-")