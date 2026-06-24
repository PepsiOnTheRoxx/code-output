import pytest
from unittest.mock import patch, MagicMock
from src.services.gebruikerread import GebruikerService
from src.services.gebruikerread_exceptions import GebruikerNietGevondenException, OnbekendeFoutException

def test_haal_gebruiker_op_by_id_succes():
    gebruiker_data = {'id': 1, 'naam': 'Jan'}
    with patch('src.services.gebruikerread.GebruikerRepository') as MockRepo:
        instance = MockRepo.return_value
        instance.get_gebruiker_by_id.return_value = gebruiker_data
        service = GebruikerService()
        result = service.haal_gebruiker_op_by_id(1)
        assert result == gebruiker_data
        instance.get_gebruiker_by_id.assert_called_once_with(1)

def test_haal_gebruiker_op_by_id_niet_gevonden():
    with patch('src.services.gebruikerread.GebruikerRepository') as MockRepo:
        instance = MockRepo.return_value
        instance.get_gebruiker_by_id.return_value = None
        service = GebruikerService()
        with pytest.raises(GebruikerNietGevondenException):
            service.haal_gebruiker_op_by_id(999)

def test_haal_alle_gebruikers_succes():
    gebruikers_lijst = [
        {'id': 1, 'naam': 'Jan'},
        {'id': 2, 'naam': 'Piet'},
    ]
    with patch('src.services.gebruikerread.GebruikerRepository') as MockRepo:
        instance = MockRepo.return_value
        instance.get_alle_gebruikers.return_value = gebruikers_lijst
        service = GebruikerService()
        result = service.haal_alle_gebruikers()
        assert result == gebruikers_lijst
        instance.get_alle_gebruikers.assert_called_once()

def test_haal_alle_gebruikers_leeg():
    with patch('src.services.gebruikerread.GebruikerRepository') as MockRepo:
        instance = MockRepo.return_value
        instance.get_alle_gebruikers.return_value = []
        service = GebruikerService()
        result = service.haal_alle_gebruikers()
        assert result == []
        instance.get_alle_gebruikers.assert_called_once()

def test_haal_gebruiker_op_by_id_onbekende_fout():
    with patch('src.services.gebruikerread.GebruikerRepository') as MockRepo:
        instance = MockRepo.return_value
        instance.get_gebruiker_by_id.side_effect = Exception("Database down")
        service = GebruikerService()
        with pytest.raises(OnbekendeFoutException):
            service.haal_gebruiker_op_by_id(1)

def test_haal_alle_gebruikers_onbekende_fout():
    with patch('src.services.gebruikerread.GebruikerRepository') as MockRepo:
        instance = MockRepo.return_value
        instance.get_alle_gebruikers.side_effect = Exception("DB error")
        service = GebruikerService()
        with pytest.raises(OnbekendeFoutException):
            service.haal_alle_gebruikers()