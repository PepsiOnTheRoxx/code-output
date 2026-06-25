from flask import Blueprint, render_template, redirect, url_for, request
import sqlite3, os

catalogusfrontend_bp = Blueprint('catalogusfrontend', __name__)
DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'bibliotheek.db')

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
def detail(boek_id):
    conn = get_db()
    boek = conn.execute('SELECT * FROM boeken WHERE id=?', (boek_id,)).fetchone()
    conn.close()
    return render_template('boekdetailfrontend.html', boek=boek)

@catalogusfrontend_bp.route('/boek/nieuw', methods=['GET', 'POST'])
def toevoegen():
    if request.method == 'POST':
        conn = get_db()
        conn.execute('INSERT INTO boeken (titel, auteur, kaft_url, status) VALUES (?, ?, ?, ?)',
                     (request.form['titel'], request.form['auteur'], request.form['kaft_url'], request.form['status']))
        conn.commit()
        boek_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
        conn.close()
        return redirect(url_for('catalogusfrontend.detail', boek_id=boek_id))
    return render_template('boektoevoegenfrontend.html')

@catalogusfrontend_bp.route('/boek/<int:boek_id>/aanpassen', methods=['GET', 'POST'])
def aanpassen(boek_id):
    conn = get_db()
    if request.method == 'POST':
        conn.execute('UPDATE boeken SET titel=?, auteur=?, kaft_url=?, status=? WHERE id=?',
                     (request.form['titel'], request.form['auteur'], request.form['kaft_url'], request.form['status'], boek_id))
        conn.commit()
        conn.close()
        return redirect(url_for('catalogusfrontend.detail', boek_id=boek_id))
    boek = conn.execute('SELECT * FROM boeken WHERE id=?', (boek_id,)).fetchone()
    conn.close()
    return render_template('boekaapassenfrontend.html', boek=boek)
