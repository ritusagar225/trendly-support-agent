from app.tools.returns import check_return_eligibility


def test_valid_return():
    result = check_return_eligibility(
        "TR-4530",
        "2026-08-24"
    )

    assert result["eligible"] is True
    assert result["action"] == "return_eligible"


def test_non_returnable_jewellery():
    result = check_return_eligibility(
        "TR-4527",
        "2026-08-24"
    )

    assert result["eligible"] is False
    assert result["action"] == "not_eligible"


def test_expired_return():
    result = check_return_eligibility(
        "TR-4523",
        "2026-08-24"
    )

    assert result["eligible"] is False
    assert result["action"] == "not_eligible"


def test_cancelled_order():
    result = check_return_eligibility(
        "TR-4529",
        "2026-08-24"
    )

    assert result["eligible"] is False
    assert result["action"] == "no_return"


def test_final_sale_item():
    result = check_return_eligibility(
        "TR-4528",
        "2026-08-10"
    )

    assert result["eligible"] is False
    assert result["action"] == "exchange_only"