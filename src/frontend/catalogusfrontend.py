from flask import Blueprint, render_template, redirect, url_for, request
import sqlite3
from database import get_connection, DB_PATH

catalogusfrontend_bp = Blueprint('catalogusfrontend', __name__)

def get_db():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    return conn

@catalogusfrontend_bp.route('/')
def catalogus_frontend():
    conn = get_db()
    boeken = conn.execute('SELECT rowid as id, * FROM boeken').fetchall()
    conn.close()
    return render_template('catalogus_frontend.html', boeken=boeken)

@catalogusfrontend_bp.route('/boek/<int:boek_id>')
def boek_detail_frontend(boek_id):
    conn = get_db()
    boek = conn.execute('SELECT rowid as id, * FROM boeken WHERE rowid=?', (boek_id,)).fetchone()
    conn.close()
    return render_template('boek_detail_frontend.html', boek=boek)

@catalogusfrontend_bp.route('/boek/toevoegen', methods=['GET', 'POST'])
def boek_toevoegen_frontend():
    if request.method == 'POST':
        titel = request.form['titel']
        auteur = request.form['auteur']
        # Vul overige verplichte kolommen met None of een default
        conn = get_db()
        conn.execute('INSERT INTO boeken (titel, auteur, beschrijving, is_uitgeleend, isbn, kaft_foto_url, publicatiedatum, uitgeleend_datum, uitgeleend_max_tot) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (titel, auteur, None, None, None, None, None, None, None))
        conn.commit()
        boek_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
        conn.close()
        return redirect(url_for('catalogusfrontend.boek_detail_frontend', boek_id=boek_id))
    return render_template('boek_toevoegen_frontend.html')

@catalogusfrontend_bp.route('/boek/<int:boek_id>/aanpassen', methods=['GET', 'POST'])
def boek_aanpassen_frontend(boek_id):
    conn = get_db()
    if request.method == 'POST':
        titel = request.form['titel']
        auteur = request.form['auteur']
        conn.execute('UPDATE boeken SET titel=?, auteur=? WHERE rowid=?', (titel, auteur, boek_id))
        conn.commit()
        conn.close()
        return redirect(url_for('catalogusfrontend.boek_detail_frontend', boek_id=boek_id))
    boek = conn.execute('SELECT rowid as id, * FROM boeken WHERE rowid=?', (boek_id,)).fetchone()
    conn.close()
    return render_template('boek_aanpassen_frontend.html', boek=boek)
