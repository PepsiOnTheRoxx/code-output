import pytest
from flask import Flask
from src.frontend.boekdetailfrontend import boekdetailfrontend_bp
import sqlite3
import os
from jinja2 import DictLoader

def setup_test_db():
    db_path = 'test_boeken.db'
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS boeken (
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
    c.execute('''CREATE TABLE IF NOT EXISTS uitleen (
        id INTEGER PRIMARY KEY,
        boek_id INTEGER,
        uitgeleend_aan TEXT
    )''')
    c.execute('DELETE FROM boeken')  # Ensure clean slate
    c.execute('DELETE FROM uitleen')
    c.execute('''INSERT INTO boeken (titel, auteur, isbn, beschrijving, is_uitgeleend, kaft_foto_url, publicatiedatum, uitgeleend_datum, uitgeleend_max_tot)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              ('De Grote Reis', 'Jan Tester', 'ISBN123', '', 0, 'https://img.test/kaft.jpg', '2023-01-01', None, None))
    c.execute('''INSERT INTO uitleen (id, boek_id, uitgeleend_aan)
                 VALUES (1, 1, 'Lisa')''')
    conn.commit()
    conn.close()
    return db_path

def remove_test_db(db_path):
    try:
        os.remove(db_path)
    except FileNotFoundError:
        pass

def test_boekdetail_page(monkeypatch, tmp_path):
    db_path = os.path.join(tmp_path, 'db.sqlite')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE boeken (
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
    c.execute('''CREATE TABLE uitleen (
        id INTEGER PRIMARY KEY,
        boek_id INTEGER,
        uitgeleend_aan TEXT
    )''')
    c.execute('''INSERT INTO boeken (titel, auteur, isbn, beschrijving, is_uitgeleend, kaft_foto_url, publicatiedatum, uitgeleend_datum, uitgeleend_max_tot)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              ("Some Titel", "Jan Auteur", "XXYY", "", 0, "https://img.link/kaft.png", "2020-01-01", None, None))
    c.execute('''INSERT INTO uitleen VALUES (1, 1, "Pietje")''')
    conn.commit()
    conn.close()

    from src.frontend import boekdetailfrontend
    monkeypatch.setattr(boekdetailfrontend, 'get_connection', lambda: sqlite3.connect(db_path))

    app = Flask(__name__)
    app.register_blueprint(boekdetailfrontend_bp)

    @app.route('/aanpassen/<int:boek_id>')
    def aanpassen(boek_id):
        return f"Aanpassen {boek_id}"
    app.add_url_rule('/catalogus', endpoint='catalogusfrontend.index', view_func=lambda: "Catalogus")
    app.add_url_rule('/boekaanpassen/<int:boek_id>', endpoint='boekaanpassenfrontend.aanpassen', view_func=lambda boek_id: f"Boek aanpassen: {boek_id}")

    # Add a minimal template for test (shows all needed fields + links)
    app.jinja_loader = DictLoader({
        'boek_detail.html': '''
<html>
    <body>
        <h1>{{ boek.titel }}</h1>
        <p>Auteur: {{ boek.auteur }}</p>
        <p>ISBN: {{ boek.isbn }}</p>
        <p>Kaft: <img src="{{ boek.kaft_foto_url }}"></p>
        <p>Publicatiedatum: {{ boek.publicatiedatum }}</p>
        {% if uitleen %}
            <p>Uitgeleend aan: {{ uitleen.uitgeleend_aan }}</p>
        {% else %}
            <p>Niet uitgeleend</p>
        {% endif %}
        <a href="{{ aanpassen_url }}">Aanpassen</a>
        <a href="{{ catalogus_url }}">Catalogus</a>
    </body>
</html>
'''
    })

    with app.test_client() as c:
        r = c.get('/boek/1')
        assert r.status_code == 200
        html = r.get_data(as_text=True)
        assert 'Some Titel' in html
        assert 'Jan Auteur' in html
        assert 'https://img.link/kaft.png' in html
        assert 'XXYY' in html
        assert '2020-01-01' in html
        assert 'Pietje' in html
        assert '/boekaanpassen/1' in html or '/aanpassen/1' in html
        assert '/catalogus' in html

def test_boekdetail_not_found(monkeypatch, tmp_path):
    db_path = os.path.join(tmp_path, 'db.sqlite')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE boeken (
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
    c.execute('''CREATE TABLE uitleen (
        id INTEGER PRIMARY KEY,
        boek_id INTEGER,
        uitgeleend_aan TEXT
    )''')
    conn.commit()
    conn.close()
    from src.frontend import boekdetailfrontend
    monkeypatch.setattr(boekdetailfrontend, 'get_connection', lambda: sqlite3.connect(db_path))
    app = Flask(__name__)
    app.register_blueprint(boekdetailfrontend_bp)
    # Fallback minimal template for 404 errors
    app.jinja_loader = DictLoader({
        'boek_detail.html': "NVT"
    })
    with app.test_client() as c:
        r = c.get('/boek/999')
        assert r.status_code == 404
        assert "Boek niet gevonden" in r.get_data(as_text=True)
