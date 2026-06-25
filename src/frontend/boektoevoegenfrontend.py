from flask import Blueprint, render_template, redirect, url_for, request
import sqlite3
from database import get_connection, DB_PATH

boektoevoegenfrontend_bp = Blueprint('boektoevoegenfrontend', __name__)

def get_db():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    return conn

@boektoevoegenfrontend_bp.route('/boek/nieuw', methods=['GET', 'POST'])
def boek_toevoegen():
    if request.method == 'POST':
        titel = request.form['titel']
        auteur = request.form['auteur']
        jaar = request.form['jaar']
        uitgever = request.form['uitgever']
        kaft_foto_url = request.form['kaft_foto_url']
        conn = get_db()
        cur = conn.cursor()
        cur.execute('INSERT INTO boeken (titel, auteur, jaar, uitgever, kaft_foto_url) VALUES (?, ?, ?, ?, ?)',
                    (titel, auteur, jaar, uitgever, kaft_foto_url))
        conn.commit()
        boek_id = cur.lastrowid
        conn.close()
        return redirect(url_for('boektoevoegenfrontend.boek_detail', boek_id=boek_id))
    return render_template('boek_toevoegen.html')

@boektoevoegenfrontend_bp.route('/boek/<int:boek_id>')
def boek_detail(boek_id):
    conn = get_db()
    boek = conn.execute('SELECT * FROM boeken WHERE id=?', (boek_id,)).fetchone()
    conn.close()
    return render_template('boek_detail.html', boek=boek)
