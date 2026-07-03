"""Scheduler helpers for CraigSail — retrieve saved searches ready to be polled."""
import json
from typing import Dict
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


async def run_scheduling_pass(db: DBSession, scraper) -> Dict[int, int]:
    """Execute the actual search across selected cities for each saved search.

    Returns a dict mapping saved-search id to hit count.
    """
    selected = select_scheduled(db)
    results: Dict[int, int] = {}
    for saved in selected:
        cities_json = saved.cities or "[]"
        cities = json.loads(cities_json) if saved.cities else []
        for city in cities:
            hits = await scraper.search(saved.query, city)
            results[saved.id] = hits
    return results
