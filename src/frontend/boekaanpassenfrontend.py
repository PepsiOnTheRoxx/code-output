from flask import Blueprint, render_template, redirect, url_for, request
import sqlite3
from database import get_connection, DB_PATH

boekaanpassenfrontend_bp = Blueprint('boekaanpassenfrontend', __name__)

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@boekaanpassenfrontend_bp.route('/boek/<int:boek_id>/aanpassen', methods=['GET', 'POST'])
def aanpassen(boek_id):
    conn = get_db()
    boek = conn.execute('SELECT rowid as id, * FROM boeken WHERE rowid = ?', (boek_id,)).fetchone()
    if not boek:
        conn.close()
        return render_template('404.html'), 404
    if request.method == 'POST':
        # Alleen kolommen in het schema updaten
        titel = request.form['titel']
        auteur = request.form['auteur']
        beschrijving = request.form.get('beschrijving', '')
        is_uitgeleend = request.form.get('is_uitgeleend', 0)
        isbn = request.form['isbn']
        kaft_foto_url = request.form.get('kaft_foto_url', '')
        publicatiedatum = request.form.get('publicatiedatum', '')
        uitgeleend_datum = request.form.get('uitgeleend_datum', None)
        uitgeleend_max_tot = request.form.get('uitgeleend_max_tot', None)
        conn.execute('''UPDATE boeken SET titel=?, auteur=?, beschrijving=?, is_uitgeleend=?, isbn=?, kaft_foto_url=?, publicatiedatum=?, uitgeleend_datum=?, uitgeleend_max_tot=? WHERE rowid=?''',
                     (titel, auteur, beschrijving or None, is_uitgeleend, isbn, kaft_foto_url or None, publicatiedatum or None, uitgeleend_datum, uitgeleend_max_tot, boek_id))
        conn.commit()
        conn.close()
        return redirect(url_for('boekaanpassenfrontend.detail', boek_id=boek_id))
    conn.close()
    return render_template('boek_aanpassen.html', boek=boek)

@boekaanpassenfrontend_bp.route('/boek/<int:boek_id>')
def detail(boek_id):
    conn = get_db()
    boek = conn.execute('SELECT rowid as id, * FROM boeken WHERE rowid = ?', (boek_id,)).fetchone()
    conn.close()
    if not boek:
        return render_template('404.html'), 404
    return render_template('boek_detail.html', boek=boek)
