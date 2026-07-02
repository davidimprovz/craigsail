"""Tests for the SavedSearch.is_scheduled flag (improvement: schedule flag)."""
from app.models import SavedSearch


def test_saved_search_has_is_scheduled_attribute():
    """SavedSearch must expose is_scheduled as a model field."""
    assert "is_scheduled" in SavedSearch.model_fields


def test_saved_search_default_is_scheduled_false():
    """A freshly-created SavedSearch should have is_scheduled = False by default."""
    ss = SavedSearch(cities=["sf"], query="bike")
    assert "is_scheduled" in SavedSearch.model_fields
    assert ss.is_scheduled is False


def test_saved_search_is_scheduled_default_value():
    """The default value of is_scheduled should be False."""
    ss = SavedSearch(cities=["sf"], query="bike", is_scheduled=True)
    assert ss.is_scheduled is True
    assert "is_scheduled" in SavedSearch(cities=["sf"], query="bike").model_dump()
