from flask import Blueprint, render_template, redirect, url_for, request
import sqlite3
from database import get_connection, DB_PATH

boektoevoegenfrontend_bp = Blueprint('boektoevoegenfrontend', __name__)

def get_db():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    return conn

@boektoevoegenfrontend_bp.route('/boek/toevoegen', methods=['GET', 'POST'])
def toevoegen():
    if request.method == 'POST':
        auteur = request.form.get('auteur')
        beschrijving = request.form.get('beschrijving')
        titel = request.form.get('titel')
        isbn = request.form.get('isbn')
        publicatiedatum = request.form.get('publicatiedatum')
        kaft_foto_url = request.form.get('kaft_foto_url')
        is_uitgeleend = 1 if request.form.get('is_uitgeleend') == 'on' else 0
        uitgeleend_datum = request.form.get('uitgeleend_datum') or None
        uitgeleend_max_tot = request.form.get('uitgeleend_max_tot') or None

        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO boeken (auteur, beschrijving, titel, isbn, publicatiedatum, kaft_foto_url, is_uitgeleend, uitgeleend_datum, uitgeleend_max_tot) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (
                auteur,
                beschrijving,
                titel,
                isbn,
                publicatiedatum,
                kaft_foto_url,
                is_uitgeleend,
                uitgeleend_datum,
                uitgeleend_max_tot
            )
        )
        conn.commit()
        boek_id = cur.lastrowid
        conn.close()
        return redirect(url_for('boekdetailfrontend.detail', boek_id=boek_id))
    return render_template('boek_toevoegen.html')
