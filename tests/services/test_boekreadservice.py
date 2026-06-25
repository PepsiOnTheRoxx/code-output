import pytest
from unittest.mock import patch, MagicMock
from src.services.boekreadservice import BoekReadService
from src.services.boekreadservice_exceptions import BoekNotFoundException, DatabaseReadException

@pytest.fixture
def mock_db_session():
    return MagicMock()

@pytest.fixture
def boekreadservice(mock_db_session):
    return BoekReadService(db_session=mock_db_session)

def test_get_boek_by_id_returns_boek(boekreadservice, mock_db_session):
    boek_id = 10
    boek = {'id': boek_id, 'titel': 'Test Boek'}
    mock_db_session.query.return_value.get.return_value = boek
    result = boekreadservice.get_boek_by_id(boek_id)
    assert result == boek
    mock_db_session.query.assert_called()
    mock_db_session.query.return_value.get.assert_called_with(boek_id)

def test_get_boek_by_id_raises_not_found(boekreadservice, mock_db_session):
    boek_id = 20
    mock_db_session.query.return_value.get.return_value = None
    with pytest.raises(BoekNotFoundException):
        boekreadservice.get_boek_by_id(boek_id)

def test_get_all_boeken_returns_list(boekreadservice, mock_db_session):
    boeken = [
        {'id': 1, 'titel': 'Boek1'},
        {'id': 2, 'titel': 'Boek2'}
    ]
    mock_db_session.query.return_value.all.return_value = boeken
    result = boekreadservice.get_all_boeken()
    assert result == boeken
    mock_db_session.query.assert_called()
    mock_db_session.query.return_value.all.assert_called()

def test_get_all_boeken_returns_empty_list(boekreadservice, mock_db_session):
    mock_db_session.query.return_value.all.return_value = []
    result = boekreadservice.get_all_boeken()
    assert result == []

def test_get_boek_by_id_database_exception(boekreadservice, mock_db_session):
    boek_id = 25
    mock_db_session.query.return_value.get.side_effect = Exception('db error')
    with pytest.raises(DatabaseReadException):
        boekreadservice.get_boek_by_id(boek_id)

def test_get_all_boeken_database_exception(boekreadservice, mock_db_session):
    mock_db_session.query.return_value.all.side_effect = Exception('db error')
    with pytest.raises(DatabaseReadException):
        boekreadservice.get_all_boeken()