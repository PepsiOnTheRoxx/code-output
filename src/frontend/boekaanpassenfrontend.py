from flask import Blueprint, render_template, redirect, url_for, request
import sqlite3
from database import get_connection, DB_PATH

boekaanpassenfrontend_bp = Blueprint('boekaanpassenfrontend', __name__)

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@boekaanpassenfrontend_bp.route('/boek/<int:boek_id>/aanpassen', methods=['GET', 'POST'])
def aanpassen(boek_id):
    conn = get_db()
    boek = conn.execute('SELECT * FROM boeken WHERE id = ?', (boek_id,)).fetchone()
    if not boek:
        conn.close()
        return render_template('404.html'), 404
    if request.method == 'POST':
        titel = request.form['titel']
        auteur = request.form['auteur']
        jaar = request.form['jaar']
        uitgever = request.form['uitgever']
        uitleen_status = request.form.get('uitleen_status', 'beschikbaar')
        conn.execute('''UPDATE boeken SET titel=?, auteur=?, jaar=?, uitgever=?, uitleen_status=? WHERE id=?''',
                     (titel, auteur, jaar, uitgever, uitleen_status, boek_id))
        conn.commit()
        conn.close()
        return redirect(url_for('boekaanpassenfrontend.detail', boek_id=boek_id))
    conn.close()
    return render_template('boek_aanpassen.html', boek=boek)

@boekaanpassenfrontend_bp.route('/boek/<int:boek_id>')
def detail(boek_id):
    conn = get_db()
    boek = conn.execute('SELECT * FROM boeken WHERE id = ?', (boek_id,)).fetchone()
    conn.close()
    if not boek:
        return render_template('404.html'), 404
    return render_template('boek_detail.html', boek=boek)
