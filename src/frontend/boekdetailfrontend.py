from flask import Blueprint, render_template, redirect, url_for, request
import sqlite3, os

boekdetailfrontend_bp = Blueprint('boekdetailfrontend', __name__)
DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'bibliotheek.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@boekdetailfrontend_bp.route('/boek/<int:boek_id>')
def detail(boek_id):
    conn = get_db()
    boek = conn.execute('SELECT * FROM boeken WHERE id = ?', (boek_id,)).fetchone()
    uitleen = conn.execute('SELECT * FROM uitleningen WHERE boek_id = ? AND retourdatum IS NULL', (boek_id,)).fetchone()
    conn.close()
    return render_template('boek_detail.html', boek=boek, uitleen=uitleen)
