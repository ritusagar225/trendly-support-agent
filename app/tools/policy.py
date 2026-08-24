from pathlib import Path
import re


POLICY_PATH = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "trendly_policy.md"
)


SECTION_KEYWORDS = {
    "1. Shipping": {
        "shipping",
        "ship",
        "shipped",
        "dispatch",
        "delivery",
        "delivered",
        "carrier",
        "tracking",
        "parcel",
        "lost",
        "delayed",
        "delay",
        "address",
        "backorder",
        "backordered",
    },
    "2. Returns": {
        "return",
        "returns",
        "returned",
        "returnable",
        "jewellery",
        "innerwear",
        "socks",
        "beauty",
        "fragrance",
        "mask",
        "gift card",
        "final sale",
        "footwear",
        "shoe",
        "cancelled",
        "condition",
        "tags",
        "packaging",
    },
    "3. Refunds": {
        "refund",
        "refunds",
        "refunded",
        "upi",
        "card",
        "credit card",
        "debit card",
        "cash on delivery",
        "cod",
        "bank",
        "payment",
        "shipping fee",
        "inspection",
    },
    "4. Exchanges": {
        "exchange",
        "exchanges",
        "size",
        "colour",
        "color",
        "style",
        "second exchange",
    },
    "5. Return pickup": {
        "pickup",
        "pick-up",
        "courier",
        "self-ship",
        "self ship",
        "serviceable",
        "pincode",
        "failed pickup",
    },
    "6. Damaged or wrong items": {
        "damaged",
        "damage",
        "defective",
        "wrong item",
        "incorrect item",
        "photograph",
        "photos",
        "replacement",
        "48 hours",
    },
}


def load_policy() -> str:
    """Load the provided Trendly policy without modifying it."""
    with open(POLICY_PATH, "r", encoding="utf-8") as file:
        return file.read()


def _extract_sections(policy: str) -> dict[str, str]:
    """
    Extract top-level ## sections while preserving
    their original content.
    """
    matches = list(
        re.finditer(r"^## (.+)$", policy, re.MULTILINE)
    )

    sections = {}

    for index, match in enumerate(matches):
        title = match.group(1).strip()

        start = match.start()
        end = (
            matches[index + 1].start()
            if index + 1 < len(matches)
            else len(policy)
        )

        sections[title] = policy[start:end].strip()

    return sections


def _normalise(text: str) -> str:
    """Normalise text for deterministic matching."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s-]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def search_policy(query: str) -> str:
    """
    Retrieve the most relevant policy sections.

    This function retrieves policy text only.
    It does not generate, infer, or invent policy.
    """
    policy = load_policy()
    sections = _extract_sections(policy)

    query_normalised = _normalise(query)

    matches = []

    for section_name, keywords in SECTION_KEYWORDS.items():
        score = 0

        for keyword in keywords:
            keyword_normalised = _normalise(keyword)

            if keyword_normalised in query_normalised:
                score += 1

        if score > 0:
            matches.append(
                (score, section_name)
            )

    if not matches:
        return (
            "NO_POLICY_MATCH: The Trendly policy does not cover "
            "this question. Do not infer or invent a policy answer. "
            "Offer a human support agent."
        )

    # Highest scoring sections first.
    matches.sort(
        key=lambda item: item[0],
        reverse=True
    )

    # Only return sections with the highest score.
    highest_score = matches[0][0]

    selected_sections = [
        section_name
        for score, section_name in matches
        if score == highest_score
    ]

    return "\n\n".join(
        sections[section_name]
        for section_name in selected_sections
        if section_name in sections
    )


