from flask import Blueprint, render_template, redirect, url_for, request
import sqlite3
from database import get_connection, DB_PATH

boektoevoegenfrontend_bp = Blueprint('boektoevoegenfrontend', __name__)

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@boektoevoegenfrontend_bp.route('/boek/nieuw', methods=['GET', 'POST'])
def toevoegen():
    if request.method == 'POST':
        titel = request.form['titel']
        auteur = request.form['auteur']
        jaar = request.form['jaar']
        isbn = request.form['isbn']
        conn = get_db()
        conn.execute('INSERT INTO boeken (titel, auteur, jaar, isbn) VALUES (?, ?, ?, ?)', (titel, auteur, jaar, isbn))
        conn.commit()
        boek_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
        conn.close()
        return redirect(url_for('boekdetailfrontend.detail', boek_id=boek_id))
    return render_template('boek_toevoegen.html')
