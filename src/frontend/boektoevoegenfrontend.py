from flask import Blueprint, render_template, redirect, url_for, request
import sqlite3, os

boektoevoegenfrontend_bp = Blueprint('boektoevoegenfrontend', __name__)
DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'boeken.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@boektoevoegenfrontend_bp.route('/boek/toevoegen', methods=['GET', 'POST'])
def boek_toevoegen():
    if request.method == 'POST':
        titel = request.form['titel']
        auteur = request.form['auteur']
        uitgever = request.form['uitgever']
        publicatiejaar = request.form['publicatiejaar']
        kaft_url = request.form['kaft_url']
        conn = get_db()
        conn.execute('INSERT INTO boeken (titel, auteur, uitgever, publicatiejaar, kaft_url) VALUES (?, ?, ?, ?, ?)',
                     (titel, auteur, uitgever, publicatiejaar, kaft_url))
        conn.commit()
        boek_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
        conn.close()
        return redirect(url_for('boektoevoegenfrontend.boek_detail', boek_id=boek_id))
    return render_template('boek_toevoegen.html')

@boektoevoegenfrontend_bp.route('/')
def catalogus():
    conn = get_db()
    boeken = conn.execute('SELECT * FROM boeken').fetchall()
    conn.close()
    return render_template('catalogus.html', boeken=boeken)

@boektoevoegenfrontend_bp.route('/boek/<int:boek_id>')
def boek_detail(boek_id):
    conn = get_db()
    boek = conn.execute('SELECT * FROM boeken WHERE id=?', (boek_id,)).fetchone()
    conn.close()
    return render_template('boek_detail.html', boek=boek)

@boektoevoegenfrontend_bp.route('/boek/<int:boek_id>/aanpassen', methods=['GET', 'POST'])
def boek_aanpassen(boek_id):
    conn = get_db()
    if request.method == 'POST':
        titel = request.form['titel']
        auteur = request.form['auteur']
        uitgever = request.form['uitgever']
        publicatiejaar = request.form['publicatiejaar']
        kaft_url = request.form['kaft_url']
        conn.execute('UPDATE boeken SET titel=?, auteur=?, uitgever=?, publicatiejaar=?, kaft_url=? WHERE id=?',
                     (titel, auteur, uitgever, publicatiejaar, kaft_url, boek_id))
        conn.commit()
        conn.close()
        return redirect(url_for('boektoevoegenfrontend.boek_detail', boek_id=boek_id))
    boek = conn.execute('SELECT * FROM boeken WHERE id=?', (boek_id,)).fetchone()
    conn.close()
    return render_template('boek_aanpassen.html', boek=boek)
