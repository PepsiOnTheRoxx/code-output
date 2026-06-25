from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3, os

boekaanpassenfrontend_bp = Blueprint('boekaanpassenfrontend', __name__)
DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'bibliotheek.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@boekaanpassenfrontend_bp.route('/boek/<int:boek_id>/aanpassen', methods=['GET', 'POST'])
def aanpassen(boek_id):
    conn = get_db()
    if request.method == 'POST':
        titel = request.form['titel']
        auteur = request.form['auteur']
        uitgeleend = 1 if request.form.get('uitgeleend') == 'on' else 0
        conn.execute('UPDATE boeken SET titel=?, auteur=?, uitgeleend=? WHERE id=?',
                     (titel, auteur, uitgeleend, boek_id))
        conn.commit()
        conn.close()
        return redirect(url_for('boekdetailfrontend.detail', boek_id=boek_id))
    boek = conn.execute('SELECT * FROM boeken WHERE id=?', (boek_id,)).fetchone()
    conn.close()
    return render_template('boek_aanpassen.html', boek=boek)
