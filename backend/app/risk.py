"""Pure-stdlib scam risk scoring for Craigslist listings."""


def risk_score(listing: dict, typical_price=None) -> int:
    """Return a deterministic 0-100 scam-risk score for *listing*.

    Parameters
    ----------
    listing : dict
        A listing with keys like ``price``, ``title``, ``description``, ``images``.
    typical_price : float or None
        The expected/typical market price; used to flag unusually cheap listings.

    Returns
    -------
    int
        0 (clean) through 100 (definitely suspicious).
    """
    score = 0

    # Flag listings priced well below the typical market value.
    if typical_price and listing.get("price") and listing["price"] < 0.2 * typical_price:
        score += 40

    # Flag suspicious payment/shipping keywords in title or description.
    text = (listing.get("title", "") + " " + listing.get("description", "")).lower()
    if any(k in text for k in ["wire transfer", "shipping only", "cashier check", "urgent"]):
        score += 30

    # Flag listings with no images.
    if not listing.get("images"):
        score += 15

    return min(score, 100)
