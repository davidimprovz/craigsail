from app.scheduler import select_scheduled
from unittest.mock import MagicMock


def test_select_scheduled_returns_two_rows():
    # arrange: mock db with two saved searches
    mock_db = MagicMock()
    fake_row1 = MagicMock(); fake_row1.id = 1
    fake_row2 = MagicMock(); fake_row2.id = 2
    mock_db.query.return_value.filter.return_value.all.return_value = [fake_row1, fake_row2]
    # act
    result = select_scheduled(mock_db)
    # assert
    assert len(result) == 2
