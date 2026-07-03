"""Tests for backend/app/risk.py — pure scam risk scoring."""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.risk import risk_score


# ── Fixtures ───────────────────────────────────────────────────────────

CLEAN = {
    "price": 500,
    "title": "Nice kayak for sale",
    "description": "Great condition, barely used.",
    "images": ["img1.jpg"],
}

CHEAP_PLUS_KEYWORDS = {
    "price": 10,
    "title": "Urgent: Boat deal!",
    "description": "Pay by wire transfer, shipping only",
    "images": [],
}

KEYWORDS_ONLY = {
    "price": 500,
    "title": "Cashier check accepted",
    "description": "",
    "images": ["x.jpg"],
}


# ── Assertions ─────────────────────────────────────────────────────────

def test_clean_listing_score_zero():
    assert risk_score(CLEAN) == 0


def test_cheap_plus_keywords_score_at_least_70():
    score = risk_score(CHEAP_PLUS_KEYWORDS, typical_price=500)
    assert score >= 70


def test_keywords_only_score_is_30():
    assert risk_score(KEYWORDS_ONLY) == 30
