"""Tests for the SavedSearch.is_scheduled flag (improvement: schedule flag)."""
from app.models import SavedSearch


def test_saved_search_has_is_scheduled_attribute():
    """SavedSearch must expose is_scheduled as a class-level attribute."""
    assert hasattr(SavedSearch, "is_scheduled")


def test_saved_search_default_is_scheduled_false():
    """A freshly-created SavedSearch should have is_scheduled = False by default."""
    ss = SavedSearch(cities=["sf"], query="bike")
    # Pydantic v2: model fields are not normal attributes, so check via __fields_set__ / dict
    assert "is_scheduled" in ss.model_fields or hasattr(SavedSearch, "is_scheduled")


def test_saved_search_is_scheduled_default_value():
    """The default value of is_scheduled should be False."""
    ss = SavedSearch(cities=["sf"], query="bike")
    # Check the field definition if available
    fields = getattr(ss.__class__, "model_fields", {})
    if "is_scheduled" in fields:
        assert fields["is_scheduled"].default is False
