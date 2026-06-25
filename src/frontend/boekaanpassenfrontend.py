from flask import Blueprint, render_template, redirect, url_for, request, abort
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
    boek = conn.execute('SELECT * FROM boeken WHERE rowid = ?', (boek_id,)).fetchone()
    if not boek:
        conn.close()
        abort(404)
    if request.method == 'POST':
        auteur = request.form.get('auteur', '')
        beschrijving = request.form.get('beschrijving', '')
        isbn = request.form.get('isbn', '')
        titel = request.form.get('titel', '')
        publicatiedatum = request.form.get('publicatiedatum', '')
        kaft_foto_url = request.form.get('kaft_foto_url', '')
        is_uitgeleend = 1 if request.form.get('is_uitgeleend') == 'on' else 0
        uitgeleend_datum = request.form.get('uitgeleend_datum', '')
        uitgeleend_max_tot = request.form.get('uitgeleend_max_tot', '')
        conn.execute('''UPDATE boeken SET auteur=?, beschrijving=?, isbn=?, titel=?, publicatiedatum=?, kaft_foto_url=?, is_uitgeleend=?, uitgeleend_datum=?, uitgeleend_max_tot=? WHERE rowid=?''',
                     (auteur, beschrijving, isbn, titel, publicatiedatum, kaft_foto_url, is_uitgeleend, uitgeleend_datum, uitgeleend_max_tot, boek_id))
        conn.commit()
        conn.close()
        return redirect(url_for('boekdetailfrontend.detail', boek_id=boek_id))
    conn.close()
    return render_template('boek_aanpassen.html', boek=boek)
