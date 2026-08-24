from app.tools.exchanges import check_exchange_eligibility


def test_valid_exchange():
    result = check_exchange_eligibility(
        order_id="TR-4530",
        requested_size="M",
        current_date="2026-08-10",
        exchange_count=0,
        available_sizes=["S", "M", "L", "XL"],
    )

    assert result["eligible"] is True
    assert result["action"] == "exchange_eligible"


def test_unavailable_size_becomes_refund():
    result = check_exchange_eligibility(
        order_id="TR-4530",
        requested_size="S",
        current_date="2026-08-10",
        exchange_count=0,
        available_sizes=["M", "L", "XL"],
    )

    assert result["eligible"] is False
    assert result["action"] == "refund"


def test_second_exchange_requires_human_approval():
    result = check_exchange_eligibility(
        order_id="TR-4530",
        requested_size="M",
        current_date="2026-08-10",
        exchange_count=1,
        available_sizes=["S", "M", "L"],
    )

    assert result["eligible"] is False
    assert result["action"] == "escalate"


def test_expired_exchange():
    result = check_exchange_eligibility(
        order_id="TR-4528",
        requested_size="XL",
        current_date="2026-08-24",
        exchange_count=0,
        available_sizes=["S", "M", "L", "XL"],
    )

    assert result["eligible"] is False
    assert result["action"] == "not_eligible"


def test_cancelled_order_cannot_be_exchanged():
    result = check_exchange_eligibility(
        order_id="TR-4529",
        requested_size="M",
        current_date="2026-08-10",
        exchange_count=0,
        available_sizes=["S", "M", "L"],
    )

    assert result["eligible"] is False
    assert result["action"] == "no_exchange"


def test_lost_parcel_requires_escalation():
    result = check_exchange_eligibility(
        order_id="TR-4526",
        requested_size="M",
        current_date="2026-08-10",
        exchange_count=0,
        available_sizes=["S", "M", "L"],
    )

    assert result["eligible"] is False
    assert result["action"] == "escalate"


def test_empty_requested_size_needs_clarification():
    result = check_exchange_eligibility(
        order_id="TR-4530",
        requested_size="",
        current_date="2026-08-10",
        exchange_count=0,
        available_sizes=["S", "M", "L"],
    )

    assert result["eligible"] is False
    assert result["action"] == "clarification_needed"