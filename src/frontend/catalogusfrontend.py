from flask import Blueprint, render_template, redirect, url_for, request
import sqlite3
from database import get_connection, DB_PATH

catalogusfrontend_bp = Blueprint('catalogusfrontend', __name__)

def get_db():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    return conn

@catalogusfrontend_bp.route('/')
def catalogus_overzicht():
    conn = get_db()
    boeken = conn.execute('SELECT rowid, auteur, kaft_foto_url, is_uitgeleend FROM boeken').fetchall()
    conn.close()
    return render_template('catalogusfrontend.html', boeken=boeken)

@catalogusfrontend_bp.route('/boek/<int:boek_id>')
def boek_detail(boek_id):
    conn = get_db()
    boek = conn.execute('SELECT rowid, auteur, kaft_foto_url, is_uitgeleend FROM boeken WHERE rowid=?', (boek_id,)).fetchone()
    conn.close()
    return render_template('boek_detailfrontend.html', boek=boek)

@catalogusfrontend_bp.route('/boek/nieuw', methods=['GET', 'POST'])
def boek_toevoegen():
    if request.method == 'POST':
        # Zet de kolomvolgorde exact zoals in het schema:
        auteur = request.form.get('auteur', '')
        beschrijving = request.form.get('beschrijving', '')
        is_uitgeleend = 1 if request.form.get('is_uitgeleend') == 'on' else 0
        isbn = request.form.get('isbn', '')
        kaft_foto_url = request.form.get('kaft_foto_url', '')
        publicatiedatum = request.form.get('publicatiedatum', '')
        titel = request.form.get('titel', '')
        uitgeleend_datum = request.form.get('uitgeleend_datum', '')
        uitgeleend_max_tot = request.form.get('uitgeleend_max_tot', '')

        conn = get_db()
        conn.execute('''INSERT INTO boeken (auteur, beschrijving, is_uitgeleend, isbn, kaft_foto_url, publicatiedatum, titel, uitgeleend_datum, uitgeleend_max_tot) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                     (auteur, beschrijving, is_uitgeleend, isbn, kaft_foto_url, publicatiedatum, titel,
                      uitgeleend_datum if uitgeleend_datum else None,
                      uitgeleend_max_tot if uitgeleend_max_tot else None))
        boek_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
        conn.commit()
        conn.close()
        return redirect(url_for('catalogusfrontend.boek_detail', boek_id=boek_id))
    return render_template('boek_toevoegenfrontend.html')

@catalogusfrontend_bp.route('/boek/<int:boek_id>/aanpassen', methods=['GET', 'POST'])
def boek_aanpassen(boek_id):
    conn = get_db()
    if request.method == 'POST':
        auteur = request.form.get('auteur', '')
        beschrijving = request.form.get('beschrijving', '')
        is_uitgeleend = 1 if request.form.get('is_uitgeleend') == 'on' else 0
        isbn = request.form.get('isbn', '')
        kaft_foto_url = request.form.get('kaft_foto_url', '')
        publicatiedatum = request.form.get('publicatiedatum', '')
        titel = request.form.get('titel', '')
        uitgeleend_datum = request.form.get('uitgeleend_datum', '')
        uitgeleend_max_tot = request.form.get('uitgeleend_max_tot', '')

        conn.execute('UPDATE boeken SET auteur=?, beschrijving=?, is_uitgeleend=?, isbn=?, kaft_foto_url=?, publicatiedatum=?, titel=?, uitgeleend_datum=?, uitgeleend_max_tot=? WHERE rowid=?',
                     (auteur, beschrijving, is_uitgeleend, isbn, kaft_foto_url, publicatiedatum, titel,
                      uitgeleend_datum if uitgeleend_datum else None,
                      uitgeleend_max_tot if uitgeleend_max_tot else None, boek_id))
        conn.commit()
        conn.close()
        return redirect(url_for('catalogusfrontend.boek_detail', boek_id=boek_id))
    boek = conn.execute('SELECT rowid, auteur, kaft_foto_url, is_uitgeleend, beschrijving, isbn, publicatiedatum, titel, uitgeleend_datum, uitgeleend_max_tot FROM boeken WHERE rowid=?', (boek_id,)).fetchone()
    conn.close()
    return render_template('boek_aanpassenfrontend.html', boek=boek)
