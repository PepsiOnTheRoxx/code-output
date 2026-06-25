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

    # Patch DB_PATH in implementation
    import src.frontend.boekdetailfrontend as frontend_impl
    frontend_impl.DB_PATH = db_path

    # Make test tables
    conn = sqlite3.connect(db_path)
    conn.execute('PRAGMA foreign_keys = OFF;')  # Just in case
    conn.executescript('''
    CREATE TABLE IF NOT EXISTS boeken (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titel TEXT,
        auteur TEXT,
        jaar TEXT
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
        c.application = app  # Typical use; allows test to inspect the Flask app
        yield c
    os.close(db_fd)
    os.unlink(db_path)

def test_index_empty(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'Boekenlijst' in rv.data or b'boeken' in rv.data or b'boek' in rv.data

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

def test_aanpassen_boek(client):
    import src.frontend.boekdetailfrontend as frontend_impl
    db_path = frontend_impl.DB_PATH
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.execute('INSERT INTO boeken (titel, auteur, jaar) VALUES (?, ?, ?)', ('Oud Titel', 'Orig Auteur', '2018'))
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
