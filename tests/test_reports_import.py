"""Verify that build_export_records is importable from app.main."""

from app.main import build_export_records


def test_build_export_records_is_callable():
    assert callable(build_export_records)
