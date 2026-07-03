import asyncio
from unittest.mock import MagicMock, AsyncMock
from app.scheduler import run_scheduling_pass


def test_run_scheduling_pass_returns_one_hit():
    # arrange
    mock_db = MagicMock()
    fake_row = MagicMock()
    fake_row.id = 42
    fake_row.cities = '["NY"]'
    fake_row.query = "test query"
    mock_db.query.return_value.filter.return_value.all.return_value = [fake_row]

    scraper = AsyncMock()
    scraper.search = AsyncMock(return_value=1)

    # act
    result = asyncio.run(run_scheduling_pass(mock_db, scraper))

    # assert
    assert isinstance(result, dict)
    assert result.get(42) == 1
