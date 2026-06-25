from flask import Blueprint, render_template, redirect, url_for, request
import sqlite3
from database import get_connection, DB_PATH

catalogusfrontend_bp = Blueprint('catalogusfrontend', __name__)

def get_db():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    return conn

@catalogusfrontend_bp.route('/')
def catalogus():
    conn = get_db()
    boeken = conn.execute('SELECT rowid as id, auteur, titel, kaft_foto_url, is_uitgeleend FROM boeken').fetchall()
    conn.close()
    return render_template('catalogus.html', boeken=boeken)

@catalogusfrontend_bp.route('/boek/<int:boek_id>')
def boek_detail(boek_id):
    conn = get_db()
    boek = conn.execute('SELECT rowid as id, auteur, titel, kaft_foto_url, is_uitgeleend FROM boeken WHERE rowid=?', (boek_id,)).fetchone()
    conn.close()
    return render_template('boek_detail.html', boek=boek)

@catalogusfrontend_bp.route('/boek/nieuw', methods=['GET', 'POST'])
def boek_toevoegen():
    if request.method == 'POST':
        auteur = request.form['auteur']
        titel = request.form['titel']
        kaft_foto_url = request.form['kaft_foto_url']
        is_uitgeleend = 1 if 'is_uitgeleend' in request.form else 0
        conn = get_db()
        conn.execute('INSERT INTO boeken (auteur, titel, kaft_foto_url, is_uitgeleend) VALUES (?, ?, ?, ?)',
                     (auteur, titel, kaft_foto_url, is_uitgeleend))
        conn.commit()
        boek_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
        conn.close()
        return redirect(url_for('catalogusfrontend.boek_detail', boek_id=boek_id))
    return render_template('boek_toevoegen.html')

@catalogusfrontend_bp.route('/boek/<int:boek_id>/aanpassen', methods=['GET', 'POST'])
def boek_aanpassen(boek_id):
    conn = get_db()
    if request.method == 'POST':
        auteur = request.form['auteur']
        titel = request.form['titel']
        kaft_foto_url = request.form['kaft_foto_url']
        is_uitgeleend = 1 if 'is_uitgeleend' in request.form else 0
        conn.execute('UPDATE boeken SET auteur=?, titel=?, kaft_foto_url=?, is_uitgeleend=? WHERE rowid=?',
                     (auteur, titel, kaft_foto_url, is_uitgeleend, boek_id))
        conn.commit()
        conn.close()
        return redirect(url_for('catalogusfrontend.boek_detail', boek_id=boek_id))
    boek = conn.execute('SELECT rowid as id, auteur, titel, kaft_foto_url, is_uitgeleend FROM boeken WHERE rowid=?', (boek_id,)).fetchone()
    conn.close()
    return render_template('boek_aanpassen.html', boek=boek)
