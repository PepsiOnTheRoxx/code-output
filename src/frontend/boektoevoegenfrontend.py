from flask import Blueprint, render_template, redirect, url_for, request
from database import get_connection, DB_PATH
import sqlite3

boektoevoegenfrontend_bp = Blueprint('boektoevoegenfrontend', __name__)

def get_db():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    return conn

@boektoevoegenfrontend_bp.route('/boek/nieuw', methods=['GET', 'POST'])
def toevoegen():
    if request.method == 'POST':
        titel = request.form.get('titel', '')
        auteur = request.form.get('auteur', '')
        beschrijving = request.form.get('beschrijving', '')
        isbn = request.form.get('isbn', '')
        publicatiedatum = request.form.get('publicatiedatum', '')
        kaft_foto_url = request.form.get('kaft_foto_url', '')
        is_uitgeleend = request.form.get('is_uitgeleend') == 'on'
        uitgeleend_datum = request.form.get('uitgeleend_datum', '')
        uitgeleend_max_tot = request.form.get('uitgeleend_max_tot', '')

        conn = get_db()
        cursor = conn.execute(
            'INSERT INTO boeken (auteur, beschrijving, titel, isbn, publicatiedatum, kaft_foto_url, is_uitgeleend, uitgeleend_datum, uitgeleend_max_tot) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (
                auteur,
                beschrijving,
                titel,
                isbn,
                publicatiedatum,
                kaft_foto_url,
                int(is_uitgeleend),
                uitgeleend_datum if uitgeleend_datum else None,
                uitgeleend_max_tot if uitgeleend_max_tot else None
            )
        )
        conn.commit()
        boek_id = cursor.lastrowid
        conn.close()
        return redirect(url_for('boekdetailfrontend.detail', boek_id=boek_id))
    return render_template('boek_toevoegen.html')
