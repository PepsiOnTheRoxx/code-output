import pytest
import sqlite3
from unittest.mock import patch, MagicMock
from database import DatabaseSetup
from database_exceptions import DatabaseSetupException

def test_database_setup_creates_boek_table():
    connection = MagicMock(spec=sqlite3.Connection)
    cursor = MagicMock()
    connection.cursor.return_value = cursor

    with patch('sqlite3.connect', return_value=connection):
        setup = DatabaseSetup('test.db')
        setup.initialize_database()

    connection.cursor.assert_called_once()
    cursor.execute.assert_any_call(
        '''
        CREATE TABLE IF NOT EXISTS boeken (
            auteur TEXT,
            beschrijving TEXT,
            is_uitgeleend BOOLEAN,
            isbn TEXT,
            kaft_foto_url TEXT,
            publicatiedatum DATE,
            titel TEXT,
            uitgeleend_datum DATE,
            uitgeleend_max_tot DATE
        )
        '''
    )
    connection.commit.assert_called_once()
    connection.close.assert_called_once()

def test_database_setup_raises_exception_on_failure():
    with patch('sqlite3.connect', side_effect=sqlite3.DatabaseError("DB error")):
        setup = DatabaseSetup('test.db')
        with pytest.raises(DatabaseSetupException) as exc:
            setup.initialize_database()
        assert "DB error" in str(exc.value)

def test_database_setup_table_already_exists():
    connection = MagicMock(spec=sqlite3.Connection)
    cursor = MagicMock()
    connection.cursor.return_value = cursor

    with patch('sqlite3.connect', return_value=connection):
        setup = DatabaseSetup('test.db')
        setup.initialize_database()
        cursor.execute.assert_any_call(
            '''
        CREATE TABLE IF NOT EXISTS boeken (
            auteur TEXT,
            beschrijving TEXT,
            is_uitgeleend BOOLEAN,
            isbn TEXT,
            kaft_foto_url TEXT,
            publicatiedatum DATE,
            titel TEXT,
            uitgeleend_datum DATE,
            uitgeleend_max_tot DATE
        )
        '''
        )

def test_database_setup_commits_and_closes_connection():
    connection = MagicMock(spec=sqlite3.Connection)
    cursor = MagicMock()
    connection.cursor.return_value = cursor

    with patch('sqlite3.connect', return_value=connection):
        setup = DatabaseSetup('test.db')
        setup.initialize_database()
        assert connection.commit.called
        assert connection.close.called

def test_database_setup_execute_raises_error():
    connection = MagicMock(spec=sqlite3.Connection)
    cursor = MagicMock()
    cursor.execute.side_effect = sqlite3.DatabaseError("execute error")
    connection.cursor.return_value = cursor

    with patch('sqlite3.connect', return_value=connection):
        setup = DatabaseSetup('test.db')
        with pytest.raises(DatabaseSetupException) as exc:
            setup.initialize_database()
        assert "execute error" in str(exc.value)
        connection.rollback.assert_called_once()
        connection.close.assert_called_once()
