from flask import Blueprint, render_template, redirect, url_for, request
import sqlite3
from database import get_connection

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
# Verwijder dubbele of overlappende detail en aanpassen-routes;
# verwijzing naar detail/anpassen verloopt via andere blueprints (zie routeregistratie in app.py).
