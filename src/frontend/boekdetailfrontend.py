from flask import Blueprint, render_template_string, redirect, url_for, request, current_app
import sqlite3, os

boekdetailfrontend_bp = Blueprint('boekdetailfrontend', __name__)

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'bibliotheek.db'))

def get_db():
    # During test, the tests patch this variable
    global DB_PATH
    return sqlite3.connect(DB_PATH)


# --- Minimal inline templates for testing ---
_boeken_index_html = '''
<!doctype html><title>Boeken Index</title>
<h1>Boekenlijst</h1>
<ul>
{% for boek in boeken %}<li>{{ boek[1] if boek['titel'] is none and boek[1] else boek['titel'] or boek[1] }}</li>{% endfor %}
</ul>
'''

_boek_detail_html = '''
<!doctype html><title>Boek detail</title>
<h1>Detail van boek</h1>
<p>{{ boek['titel'] }}</p>
<p>{{ boek['auteur'] }}</p>
<p>{{ boek['jaar'] }}</p>
{% if uitleen %}<p>Uitgeleend aan: {{ uitleen['lener'] }}</p>{% endif %}
'''

_boek_aanpassen_html = '''
<!doctype html><title>Boek aanpassen</title>
<h1>Aanpassen: {{ boek['titel'] }}</h1>
<form method="POST">
    <input name="titel" value="{{ boek['titel'] }}"><br>
    <input name="auteur" value="{{ boek['auteur'] }}"><br>
    <input name="jaar" value="{{ boek['jaar'] }}"><br>
    <input type="submit" value="Opslaan">
</form>
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
'''

# --- Routes ---
@boekdetailfrontend_bp.route('/')
def index():
    conn = get_db()
    conn.row_factory = sqlite3.Row
    boeken = conn.execute('SELECT * FROM boeken').fetchall()
    conn.close()
    return render_template_string(_boeken_index_html, boeken=boeken)


@boekdetailfrontend_bp.route('/boek/<int:boek_id>')
def detail(boek_id):
    conn = get_db()
    conn.row_factory = sqlite3.Row
    boek = conn.execute('SELECT * FROM boeken WHERE id = ?', (boek_id,)).fetchone()
    uitleen = conn.execute('SELECT * FROM uitleningen WHERE boek_id = ? AND retourdatum IS NULL', (boek_id,)).fetchone()
    conn.close()
    return render_template_string(_boek_detail_html, boek=boek, uitleen=uitleen)

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
    conn.close()
    return render_template_string(_boek_aanpassen_html, boek=boek)

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
