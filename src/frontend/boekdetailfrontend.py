from flask import Blueprint, render_template, render_template_string, redirect, url_for, request, current_app
import sqlite3, os

boekdetailfrontend_bp = Blueprint('boekdetailfrontend', __name__)

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'bibliotheek.db'))

def get_db():
    global DB_PATH
    return sqlite3.connect(DB_PATH)

# Templates
_boeken_index_html = '''
<!doctype html><title>Boeken Index</title>
<h1>Boekenlijst</h1>
<ul>
{% for boek in boeken %}<li>{{ boek['titel'] }}</li>{% endfor %}
</ul>
<a href="/boek/nieuw">Voeg nieuw boek toe</a>
'''

_boek_detail_html = '''
<!doctype html>
<html><head><title>Boek detail - {{ boek.titel }}</title></head><body>
<a href="/">&#x2190; Terug naar overzicht</a>
<h1>{{ boek.titel }}</h1>
<ul>
    <li><b>Titel:</b> {{ boek.titel }}</li>
    <li><b>Auteur:</b> {{ boek.auteur }}</li>
    <li><b>Jaar:</b> {{ boek.jaar }}</li>
    {% if boek.isbn %}<li><b>ISBN:</b> {{ boek.isbn }}</li>{% endif %}
    {% if boek.genre %}<li><b>Genre:</b> {{ boek.genre }}</li>{% endif %}
</ul>
{% if uitleen %}<div style='color:orangered;'><b>Uitgeleend aan: {{ uitleen.lener }}</b><br>uitgeleend op {{ uitleen.uitleendatum }}</div>{% else %}<div style='color:green;'>Beschikbaar</div>{% endif %}
<p>
    <a href="/boek/{{ boek.id }}/aanpassen">Bewerk boek</a>
</p>
</body></html>
'''

_boek_aanpassen_html = '''
<!doctype html><title>Boek aanpassen</title>
<h1>Aanpassen: {{ boek.titel }}</h1>
<form method="POST">
    <input name="titel" value="{{ boek.titel }}"><br>
    <input name="auteur" value="{{ boek.auteur }}"><br>
    <input name="jaar" value="{{ boek.jaar }}"><br>
    <input type="submit" value="Opslaan">
</form>
<a href="/boek/{{ boek.id }}">Annuleren</a>
'''

_boek_nieuw_html = '''
<!doctype html><title>Nieuw Boek</title>
<h1>Nieuw boek toevoegen</h1>
<form method="POST">
    <input name="titel" placeholder="Titel"><br>
    <input name="auteur" placeholder="Auteur"><br>
    <input name="jaar" placeholder="Jaar"><br>
    <input type="submit" value="Voeg toe">
</form>
<a href="/">Terug naar overzicht</a>
'''

# Conversion helpers: sqlite3.Row to attribute object (for Jinja dot-notation and get/exists checks)
def row_to_obj(row):
    if row is None:
        return None
    class AttrObj:
        def __init__(self, d):
            self.__dict__.update(d)
        def __getitem__(self, k):
            return self.__dict__[k]
        def get(self, k):
            return self.__dict__.get(k)
        def __contains__(self, k):
            return k in self.__dict__
    return AttrObj(dict(row))

# --- Routes ---
@boekdetailfrontend_bp.route('/')
def index():
    conn = get_db()
    conn.row_factory = sqlite3.Row
    boeken = conn.execute('SELECT * FROM boeken').fetchall()
    boeken_objs = [row_to_obj(boek) for boek in boeken]
    conn.close()
    return render_template_string(_boeken_index_html, boeken=boeken_objs)

@boekdetailfrontend_bp.route('/boek/<int:boek_id>')
def detail(boek_id):
    conn = get_db()
    conn.row_factory = sqlite3.Row
    boek = conn.execute('SELECT * FROM boeken WHERE id = ?', (boek_id,)).fetchone()
    uitleen = conn.execute('SELECT * FROM uitleningen WHERE boek_id = ? AND retourdatum IS NULL', (boek_id,)).fetchone()
    boek_obj = row_to_obj(boek)
    uitleen_obj = row_to_obj(uitleen)
    conn.close()
    return render_template_string(_boek_detail_html, boek=boek_obj, uitleen=uitleen_obj)

@boekdetailfrontend_bp.route('/boek/<int:boek_id>/aanpassen', methods=['GET', 'POST'])
def aanpassen(boek_id):
    conn = get_db()
    conn.row_factory = sqlite3.Row
    if request.method == 'POST':
        titel = request.form['titel']
        auteur = request.form['auteur']
        jaar = request.form['jaar']
        conn.execute('UPDATE boeken SET titel=?, auteur=?, jaar=? WHERE id=?', (titel, auteur, jaar, boek_id))
        conn.commit()
        conn.close()
        return redirect(url_for('boekdetailfrontend.detail', boek_id=boek_id))
    boek = conn.execute('SELECT * FROM boeken WHERE id = ?', (boek_id,)).fetchone()
    boek_obj = row_to_obj(boek)
    conn.close()
    return render_template_string(_boek_aanpassen_html, boek=boek_obj)

@boekdetailfrontend_bp.route('/boek/nieuw', methods=['GET', 'POST'])
def nieuw():
    if request.method == 'POST':
        titel = request.form['titel']
        auteur = request.form['auteur']
        jaar = request.form['jaar']
        conn = get_db()
        cursor = conn.execute('INSERT INTO boeken (titel, auteur, jaar) VALUES (?, ?, ?)', (titel, auteur, jaar))
        boek_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return redirect(url_for('boekdetailfrontend.detail', boek_id=boek_id))
    return render_template_string(_boek_nieuw_html)
