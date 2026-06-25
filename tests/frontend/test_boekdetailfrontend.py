import pytest
from flask import Flask
from src.frontend.boekdetailfrontend import boekdetailfrontend_bp
import sqlite3
import os
import tempfile

@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    app = Flask(__name__)
    app.config['TESTING'] = True

    import src.frontend.boekdetailfrontend as frontend_impl
    frontend_impl.DB_PATH = db_path

    # Test DB setup: add columns that might appear in real templates
    conn = sqlite3.connect(db_path)
    conn.execute('PRAGMA foreign_keys = OFF;')
    conn.executescript('''
    CREATE TABLE IF NOT EXISTS boeken (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titel TEXT,
        auteur TEXT,
        jaar TEXT,
        isbn TEXT,
        genre TEXT
    );
    CREATE TABLE IF NOT EXISTS uitleningen (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        boek_id INTEGER,
        lener TEXT,
        uitleendatum TEXT,
        retourdatum TEXT
    );
    ''')
    conn.commit()
    conn.close()

    app.register_blueprint(boekdetailfrontend_bp, url_prefix='')
    with app.test_client() as c:
        c.application = app
        yield c
    os.close(db_fd)
    os.unlink(db_path)

def test_index_empty(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'Boekenlijst' in rv.data
    assert b'Voeg nieuw boek toe' in rv.data

def test_nieuw_boek_and_redirect(client):
    rv = client.get('/boek/nieuw')
    assert rv.status_code == 200
    rv = client.post('/boek/nieuw', data={'titel': 'Testboek', 'auteur': 'AuteurX', 'jaar': '2022'}, follow_redirects=False)
    assert rv.status_code == 302
    assert '/boek/' in rv.headers['Location']
    boek_id = int(rv.headers['Location'].split('/')[-1])
    rv = client.get(f'/boek/{boek_id}')
    assert rv.status_code == 200
    assert b'Testboek' in rv.data
    assert b'AuteurX' in rv.data
    assert b'2022' in rv.data
    assert b'Terug naar overzicht' in rv.data

def test_aanpassen_boek(client):
    import src.frontend.boekdetailfrontend as frontend_impl
    db_path = frontend_impl.DB_PATH
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.execute('INSERT INTO boeken (titel, auteur, jaar, isbn, genre) VALUES (?, ?, ?, ?, ?)', ('Oud Titel', 'Orig Auteur', '2018', '123-456', 'Roman'))
    boek_id = cursor.lastrowid
    conn.commit()
    conn.close()

    rv = client.get(f'/boek/{boek_id}/aanpassen')
    assert rv.status_code == 200
    assert b'Oud Titel' in rv.data

    rv = client.post(f'/boek/{boek_id}/aanpassen', data={'titel': 'Nieuw Titel', 'auteur': 'Nieuwe Auteur', 'jaar': '2023'}, follow_redirects=False)
    assert rv.status_code == 302
    assert f'/boek/{boek_id}' in rv.headers['Location']
    rv = client.get(f'/boek/{boek_id}')
    assert rv.status_code == 200
    assert b'Nieuw Titel' in rv.data
    assert b'Nieuwe Auteur' in rv.data
    assert b'2018' not in rv.data
    assert b'ISBN' in rv.data
    assert b'123-456' in rv.data
    assert b'Roman' in rv.data
    assert b'Bewerk boek' in rv.data

def test_boek_detail_with_uitleen(client):
    import src.frontend.boekdetailfrontend as frontend_impl
    db_path = frontend_impl.DB_PATH
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.execute('INSERT INTO boeken (titel, auteur, jaar, isbn, genre) VALUES (?, ?, ?, ?, ?)', ('Zeldzaam', 'Uniek', '2024', 'ZYX-999', 'Nonfictie'))
    boek_id = cursor.lastrowid
    conn.execute('INSERT INTO uitleningen (boek_id, lener, uitleendatum, retourdatum) VALUES (?, ?, ?, NULL)', (boek_id, 'Jansen', '2024-06-20'))
    conn.commit()
    conn.close()
    rv = client.get(f'/boek/{boek_id}')
    assert rv.status_code == 200
    assert b'Uitgeleend aan: Jansen' in rv.data
    assert b'uitgeleend op 2024-06-20' in rv.data
    assert b'Beschikbaar' not in rv.data
    # navigatie
    assert b'Terug naar overzicht' in rv.data
    assert b'Bewerk boek' in rv.data
