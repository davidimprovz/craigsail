"""Test that SavedSearch.deviation_target field exists with default None."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.models import SavedSearch


def test_saved_search_deviation_target_default():
    """SavedSearch should have deviation_target defaulting to None."""
    saved = SavedSearch(cities=["sf"], query="test")
    assert saved.deviation_target is None
