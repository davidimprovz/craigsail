"""Scheduler helpers for CraigSail — retrieve saved searches ready to be polled."""
from sqlalchemy.orm import Session as DBSession
from app.db import SavedSearch as DBSavedSearch


def select_scheduled(db: DBSession):
    """Return all active saved searches that have a schedule_cron set.

    This is the entry point for the scheduling pass — it filters out any
    saved search that isn't both active and configured with a cron expression,
    so only real work gets scheduled.
    """
    return db.query(DBSavedSearch).filter(
        DBSavedSearch.is_active == True,  # noqa: E712
        DBSavedSearch.schedule_cron != None,  # noqa: E711
    ).all()
