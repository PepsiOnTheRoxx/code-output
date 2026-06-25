from flask import Blueprint, render_template, redirect, url_for, request
import sqlite3, os

catalogusfrontend_bp = Blueprint('catalogusfrontend', __name__)
DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'catalogus.db')


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@catalogusfrontend_bp.route('/')
def index():
    conn = get_db()
    boeken = conn.execute('SELECT * FROM boeken').fetchall()
    conn.close()
    return render_template('catalogusfrontend.html', boeken=boeken)

@catalogusfrontend_bp.route('/boek/<int:boek_id>')
def boek_detail(boek_id):
    conn = get_db()
    boek = conn.execute('SELECT * FROM boeken WHERE id=?', (boek_id,)).fetchone()
    conn.close()
    return render_template('boekdetailfrontend.html', boek=boek)

@catalogusfrontend_bp.route('/boek/nieuw', methods=['GET', 'POST'])
def boek_toevoegen():
    if request.method == 'POST':
        titel = request.form['titel']
        auteur = request.form['auteur']
        kaft_url = request.form['kaft_url']
        status = request.form.get('status', 'Beschikbaar')
        conn = get_db()
        conn.execute('INSERT INTO boeken (titel, auteur, kaft_url, status) VALUES (?, ?, ?, ?)',
                     (titel, auteur, kaft_url, status))
        conn.commit()
        boek_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
        conn.close()
        return redirect(url_for('catalogusfrontend.boek_detail', boek_id=boek_id))
    return render_template('boektoevoegenfrontend.html')

@catalogusfrontend_bp.route('/boek/<int:boek_id>/aanpassen', methods=['GET', 'POST'])
def boek_aanpassen(boek_id):
    conn = get_db()
    if request.method == 'POST':
        titel = request.form['titel']
        auteur = request.form['auteur']
        kaft_url = request.form['kaft_url']
        status = request.form.get('status', 'Beschikbaar')
        conn.execute('UPDATE boeken SET titel=?, auteur=?, kaft_url=?, status=? WHERE id=?',
                     (titel, auteur, kaft_url, status, boek_id))
        conn.commit()
        conn.close()
        return redirect(url_for('catalogusfrontend.boek_detail', boek_id=boek_id))
    boek = conn.execute('SELECT * FROM boeken WHERE id=?', (boek_id,)).fetchone()
    conn.close()
    return render_template('boeakaanpassenfrontend.html', boek=boek)
