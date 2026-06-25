import pytest
import sqlite3
from database import DB_PATH
from src.frontend.boektoevoegenfrontend import create_app

@pytest.fixture
def client():
    from src.frontend.boektoevoegenfrontend import ensure_db_is_initialized
    ensure_db_is_initialized()
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        conn = sqlite3.connect(DB_PATH)
        try:
            conn.execute('DELETE FROM boeken')
        except sqlite3.OperationalError:
            conn.execute('''CREATE TABLE boeken (
                  auteur TEXT,
                  beschrijving TEXT,
                  is_uitgeleend BOOLEAN,
                  isbn TEXT,
                  kaft_foto_url TEXT,
                  publicatiedatum DATE,
                  titel TEXT,
                  uitgeleend_datum DATE,
                  uitgeleend_max_tot DATE
                  )''')
        conn.commit()
        conn.close()
        yield client

def test_nieuw_boek_post_and_detail(client):
    data = {
        'titel': 'Het Boek',
        'auteur': 'Mevr. Schrijver',
        'beschrijving': 'Beschrijving test',
        'is_uitgeleend': '',
        'isbn': '9876543210',
        'kaft_foto_url': 'http://voorbeeld.nl/cover1.jpg',
        'publicatiedatum': '1999-01-01',
        'uitgeleend_datum': '',
        'uitgeleend_max_tot': ''
    }
    res = client.post('/boek/nieuw', data=data, follow_redirects=False)
    assert res.status_code == 302
    loc = res.headers['Location']
    assert '/boek/' in loc
    boek_id = int(loc.split('/boek/')[1])

    res = client.get(f'/boek/{boek_id}')
    assert b'Het Boek' in res.data
    assert b'Mevr. Schrijver' in res.data

def test_nieuw_boek_leeg_verplicht(client):
    data = {'titel': '', 'auteur': '', 'beschrijving': '', 'isbn': '', 'kaft_foto_url': '', 'publicatiedatum': '', 'is_uitgeleend': '', 'uitgeleend_datum': '', 'uitgeleend_max_tot': ''}
    res = client.post('/boek/nieuw', data=data, follow_redirects=True)
    # Moet beide validatie-fouten aangeven
    assert b'Titel is verplicht' in res.data
    assert b'Auteur is verplicht' in res.data

def test_nietgetal_publicatiedatum(client):
    data = {'titel': 'Test', 'auteur': 'Auteur', 'beschrijving': '', 'isbn': '111', 'kaft_foto_url': '', 'publicatiedatum': 'jinx', 'is_uitgeleend': '', 'uitgeleend_datum': '', 'uitgeleend_max_tot': ''}
    res = client.post('/boek/nieuw', data=data, follow_redirects=True)
    # Hier wordt publicatiedatum niet gevalideerd door de frontend, maar in een echte app kun je op "publicatiedatum" checken.
    # Hier alleen: formulier submit faalt niet, maar record wordt toegevoegd
    assert b'Test' in res.data
    assert b'Auteur' in res.data

def test_catalogus(client):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('INSERT INTO boeken (titel, auteur, beschrijving, is_uitgeleend, isbn, kaft_foto_url, publicatiedatum, uitgeleend_datum, uitgeleend_max_tot) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                ('B1', 'A1', None, 0, '321', 'url1', '2011-12-13', None, None))
    conn.commit()
    conn.close()
    res = client.get('/catalogus')
    assert b'B1' in res.data

def test_boek_aanpassen(client):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('INSERT INTO boeken (titel, auteur, beschrijving, is_uitgeleend, isbn, kaft_foto_url, publicatiedatum, uitgeleend_datum, uitgeleend_max_tot) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                ('B2', 'A2', None, 0, '222', 'url2', '2007-01-01', None, None))
    boek_id = cur.lastrowid
    conn.commit()
    conn.close()
    res = client.get(f'/boek/{boek_id}/aanpassen')
    assert b'B2' in res.data
    data = {'titel': 'B2 gewijzigd', 'auteur': 'A2', 'beschrijving': '', 'isbn': '222', 'kaft_foto_url': 'url3', 'publicatiedatum': '2010-01-01', 'is_uitgeleend': '', 'uitgeleend_datum': '', 'uitgeleend_max_tot': ''}
    res = client.post(f'/boek/{boek_id}/aanpassen', data=data, follow_redirects=True)
    assert b'B2 gewijzigd' in res.data
