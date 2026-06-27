from flask import Blueprint, render_template, redirect, url_for, request
import sqlite3
from database import get_connection, DB_PATH

boekdetailfrontend_bp = Blueprint('boekdetailfrontend', __name__)

def get_db():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    return conn

@boekdetailfrontend_bp.route('/boek/<int:boek_id>')
def detail(boek_id):
    conn = get_db()
    boek = conn.execute('SELECT rowid as id, auteur, beschrijving, isbn, publicatiedatum, kaft_foto_url, is_uitgeleend, uitgeleend_datum, uitgeleend_max_tot FROM boeken WHERE rowid=?', (boek_id,)).fetchone()
    conn.close()
    if not boek:
        return render_template('boekdetailfrontend_nietgevonden.html'), 404
    return render_template('boekdetailfrontend_detail.html', boek=boek)
