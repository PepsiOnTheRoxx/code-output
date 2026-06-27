from flask import Blueprint, render_template, redirect, url_for, request
import sqlite3
from database import get_connection, DB_PATH

boekaanpassenfrontend_bp = Blueprint('boekaanpassenfrontend', __name__)

def get_db():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    return conn

@boekaanpassenfrontend_bp.route('/boek/<int:boek_id>/aanpassen', methods=['GET', 'POST'])
def aanpassen(boek_id):
    conn = get_db()
    if request.method == 'POST':
        titel = request.form['titel']
        auteur = request.form['auteur']
        beschrijving = request.form['beschrijving']
        isbn = request.form['isbn']
        publicatiedatum = request.form['publicatiedatum']
        kaft_foto_url = request.form['kaft_foto_url']
        is_uitgeleend = 1 if request.form.get('is_uitgeleend') == 'on' else 0
        uitgeleend_datum = request.form['uitgeleend_datum'] or None
        uitgeleend_max_tot = request.form['uitgeleend_max_tot'] or None
        conn.execute('''UPDATE boeken SET titel=?, auteur=?, beschrijving=?, isbn=?, publicatiedatum=?, kaft_foto_url=?, is_uitgeleend=?, uitgeleend_datum=?, uitgeleend_max_tot=? WHERE rowid=?''',
                     (titel, auteur, beschrijving, isbn, publicatiedatum, kaft_foto_url, is_uitgeleend, uitgeleend_datum, uitgeleend_max_tot, boek_id))
        conn.commit()
        conn.close()
        return redirect(url_for('boekdetailfrontend.detail', boek_id=boek_id))
    boek = conn.execute('SELECT rowid as id, * FROM boeken WHERE rowid=?', (boek_id,)).fetchone()
    conn.close()
    return render_template('boek_aanpassen.html', boek=boek)
