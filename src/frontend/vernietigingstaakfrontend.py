from flask import Blueprint, render_template, request, redirect, url_for, flash
import requests
from src.frontend.vernietigingstaakfrontend_exceptions import VernietigingstaakNietGevonden, VernietigingstaakAPIFout

vernietigingstaak_bp = Blueprint('vernietigingstaak', __name__, template_folder='templates')

API_BASE_URL = 'http://api-service/vernietigingstaken'

@vernietigingstaak_bp.route('/vernietigingstaken')
def vernietigingstaak_lijst():
    try:
        response = requests.get(API_BASE_URL)
        if response.status_code != 200:
            raise VernietigingstaakAPIFout('Kan vernietigingstaken niet ophalen')
        taken = response.json()
    except Exception as e:
        taken = []
        flash(str(e), 'danger')
    return render_template('vernietigingstaak_lijst.html', taken=taken)

@vernietigingstaak_bp.route('/vernietigingstaak/<int:taak_id>', methods=['GET', 'POST'])
def vernietigingstaak_detail(taak_id):
    if request.method == 'POST':
        data = {
            'naam': request.form.get('naam'),
            'omschrijving': request.form.get('omschrijving')
        }
        try:
            put_response = requests.put(f"{API_BASE_URL}/{taak_id}", json=data)
            if put_response.status_code != 200:
                raise VernietigingstaakAPIFout('Fout bij bijwerken van vernietigingstaak')
            flash('Vernietigingstaak bijgewerkt', 'success')
            return redirect(url_for('vernietigingstaak.vernietigingstaak_lijst'))
        except Exception as e:
            flash(str(e), 'danger')

    try:
        response = requests.get(f"{API_BASE_URL}/{taak_id}")
        if response.status_code == 404:
            raise VernietigingstaakNietGevonden('Vernietigingstaak niet gevonden')
        if response.status_code != 200:
            raise VernietigingstaakAPIFout('Kan vernietigingstaak niet ophalen')
        taak = response.json()
    except Exception as e:
        flash(str(e), 'danger')
        taak = None
    return render_template('vernietigingstaak_detail.html', taak=taak)

@vernietigingstaak_bp.route('/vernietigingstaak/nieuw', methods=['GET', 'POST'])
def vernietigingstaak_nieuw():
    if request.method == 'POST':
        data = {
            'naam': request.form.get('naam'),
            'omschrijving': request.form.get('omschrijving')
        }
        try:
            post_response = requests.post(API_BASE_URL, json=data)
            if post_response.status_code != 201:
                raise VernietigingstaakAPIFout('Fout bij aanmaken van vernietigingstaak')
            flash('Vernietigingstaak aangemaakt', 'success')
            return redirect(url_for('vernietigingstaak.vernietigingstaak_lijst'))
        except Exception as e:
            flash(str(e), 'danger')
    return render_template('vernietigingstaak_detail.html', taak=None)