from flask import Blueprint, render_template, redirect, url_for, request
import sqlite3
from database import get_connection, DB_PATH

boekaanpassen_bp = Blueprint('boekaanpassenfrontend', __name__)

def get_db():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    return conn

@boekaanpassen_bp.route('/boek/<int:boek_id>/aanpassen', methods=['GET', 'POST'])
def aanpassen(boek_id):
    conn = get_db()
    if request.method == 'POST':
        titel = request.form['titel']
        auteur = request.form['auteur']
        genre = request.form['genre']
        jaar = request.form['jaar']
        uitgeleend = 1 if request.form.get('uitgeleend') == 'on' else 0
        conn.execute(
            'UPDATE boeken SET titel=?, auteur=?, genre=?, jaar=?, uitgeleend=? WHERE id=?',
            (titel, auteur, genre, jaar, uitgeleend, boek_id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('boekdetailfrontend.detail', boek_id=boek_id))
    boek = conn.execute('SELECT * FROM boeken WHERE id=?', (boek_id,)).fetchone()
    conn.close()
    return render_template('boek_aanpassen.html', boek=boek)