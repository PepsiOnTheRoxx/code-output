from flask import Blueprint, render_template, redirect, url_for, request, abort, current_app as app
import sqlite3
from database import get_connection, DB_PATH
from src.frontend.boekdetailfrontend_exceptions import BoekNietGevonden

boekdetailfrontend_bp = Blueprint('boekdetailfrontend', __name__)

def get_db():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    return conn

@boekdetailfrontend_bp.route('/boek/<int:boek_id>')
def detail(boek_id):
    conn = get_db()
    boek = conn.execute('SELECT * FROM boeken WHERE id=?', (boek_id,)).fetchone()
    if boek is None:
        conn.close()
        # Raise custom exception for test and catch
        raise BoekNietGevonden()
    uitleen = conn.execute('SELECT * FROM uitleen WHERE boek_id=?', (boek_id,)).fetchone()
    conn.close()
    # Render ALL boek attribute fields
    return render_template(
        'boek_detail.html',
        boek=boek,
        uitleen=uitleen,
        aanpassen_url=url_for('boekaanpassenfrontend.aanpassen', boek_id=boek_id),
        catalogus_url=url_for('catalogusfrontend.index')
    )
