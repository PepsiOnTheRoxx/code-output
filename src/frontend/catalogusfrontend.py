from flask import Blueprint, render_template, redirect, url_for, request
import sqlite3
from database import get_connection, DB_PATH

catalogusfrontend_bp = Blueprint('catalogusfrontend', __name__)

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@catalogusfrontend_bp.route('/')
def catalogus_overzicht():
    conn = get_db()
    boeken = conn.execute('SELECT rowid as id, * FROM boeken').fetchall()
    conn.close()
    return render_template('catalogus_overzicht.html', boeken=boeken)

@catalogusfrontend_bp.route('/boek/<int:boek_id>')
def boek_detail(boek_id):
    conn = get_db()
    boek = conn.execute('SELECT rowid as id, * FROM boeken WHERE rowid=?', (boek_id,)).fetchone()
    conn.close()
    return render_template('boek_detail.html', boek=boek)

@catalogusfrontend_bp.route('/boek/nieuw', methods=['GET', 'POST'])
def boek_toevoegen():
    if request.method == 'POST':
        auteur = request.form['auteur']
        beschrijving = request.form['beschrijving']
        titel = request.form['titel']
        isbn = request.form['isbn']
        publicatiedatum = request.form['publicatiedatum']
        kaft_foto_url = request.form['kaft_foto_url']
        is_uitgeleend = 1 if request.form.get('is_uitgeleend') else 0
        uitgeleend_datum = request.form['uitgeleend_datum'] or None
        uitgeleend_max_tot = request.form['uitgeleend_max_tot'] or None
        conn = get_db()
        conn.execute('INSERT INTO boeken (auteur, beschrijving, titel, isbn, publicatiedatum, kaft_foto_url, is_uitgeleend, uitgeleend_datum, uitgeleend_max_tot) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                     (auteur, beschrijving, titel, isbn, publicatiedatum, kaft_foto_url, is_uitgeleend, uitgeleend_datum, uitgeleend_max_tot))
        conn.commit()
        boek_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
        conn.close()
        return redirect(url_for('catalogusfrontend.boek_detail', boek_id=boek_id))
    return render_template('boek_toevoegen.html')

@catalogusfrontend_bp.route('/boek/<int:boek_id>/bewerken', methods=['GET', 'POST'])
def boek_aanpassen(boek_id):
    conn = get_db()
    if request.method == 'POST':
        auteur = request.form['auteur']
        beschrijving = request.form['beschrijving']
        titel = request.form['titel']
        isbn = request.form['isbn']
        publicatiedatum = request.form['publicatiedatum']
        kaft_foto_url = request.form['kaft_foto_url']
        is_uitgeleend = 1 if request.form.get('is_uitgeleend') else 0
        uitgeleend_datum = request.form['uitgeleend_datum'] or None
        uitgeleend_max_tot = request.form['uitgeleend_max_tot'] or None
        conn.execute('UPDATE boeken SET auteur=?, beschrijving=?, titel=?, isbn=?, publicatiedatum=?, kaft_foto_url=?, is_uitgeleend=?, uitgeleend_datum=?, uitgeleend_max_tot=? WHERE rowid=?',
                     (auteur, beschrijving, titel, isbn, publicatiedatum, kaft_foto_url, is_uitgeleend, uitgeleend_datum, uitgeleend_max_tot, boek_id))
        conn.commit()
        conn.close()
        return redirect(url_for('catalogusfrontend.boek_detail', boek_id=boek_id))
    boek = conn.execute('SELECT rowid as id, * FROM boeken WHERE rowid=?', (boek_id,)).fetchone()
    conn.close()
    return render_template('boek_aanpassen.html', boek=boek)
