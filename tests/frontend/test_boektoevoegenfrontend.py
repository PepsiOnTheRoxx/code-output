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
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  titel TEXT NOT NULL,
                  auteur TEXT NOT NULL,
                  jaar INTEGER,
                  uitgever TEXT,
                  kaft_foto_url TEXT
                  )''')
        conn.commit()
        conn.close()
        yield client

def test_nieuw_boek_post_and_detail(client):
    data = {
        'titel': 'Het Boek',
        'auteur': 'Mevr. Schrijver',
        'jaar': '1999',
        'uitgever': 'Uitg. Lezers',
        'kaft_foto_url': 'http://voorbeeld.nl/cover1.jpg'
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
    data = {'titel': '', 'auteur': '', 'jaar': '', 'uitgever': '', 'kaft_foto_url': ''}
    res = client.post('/boek/nieuw', data=data, follow_redirects=True)
    # Moet beide validatie-fouten aangeven
    assert b'Titel is verplicht' in res.data
    assert b'Auteur is verplicht' in res.data

def test_nietgetal_jaar(client):
    data = {'titel': 'Test', 'auteur': 'Auteur', 'jaar': 'jinx', 'uitgever': '', 'kaft_foto_url': ''}
    res = client.post('/boek/nieuw', data=data, follow_redirects=True)
    assert b'Jaar moet een getal zijn' in res.data

def test_catalogus(client):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('INSERT INTO boeken (titel, auteur, jaar, uitgever, kaft_foto_url) VALUES (?, ?, ?, ?, ?)',
                ('B1', 'A1', 2000, 'U1', 'url1'))
    conn.commit()
    conn.close()
    res = client.get('/catalogus')
    assert b'B1' in res.data

def test_boek_aanpassen(client):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('INSERT INTO boeken (titel, auteur, jaar, uitgever, kaft_foto_url) VALUES (?, ?, ?, ?, ?)',
                ('B2', 'A2', 2007, 'U2', 'url2'))
    boek_id = cur.lastrowid
    conn.commit()
    conn.close()
    res = client.get(f'/boek/{boek_id}/aanpassen')
    assert b'B2' in res.data
    data = {'titel': 'B2 gewijzigd', 'auteur': 'A2', 'jaar': '2010', 'uitgever': 'U2', 'kaft_foto_url': 'url3'}
    res = client.post(f'/boek/{boek_id}/aanpassen', data=data, follow_redirects=True)
    assert b'B2 gewijzigd' in res.data
