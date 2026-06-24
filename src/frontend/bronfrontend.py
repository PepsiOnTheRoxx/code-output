from flask import Blueprint, render_template, redirect, url_for, request, flash
import requests
from src.frontend.bronfrontend_exceptions import BronNotFoundException, BronAPIException

bronfrontend = Blueprint('bronfrontend', __name__, template_folder='templates')


API_BASE_URL = 'http://localhost:8000/api/bron/'


@bronfrontend.route('/bronnen/')
def bron_list():
    try:
        response = requests.get(API_BASE_URL)
        if response.status_code != 200:
            raise BronAPIException('Kon bronlijst niet ophalen.')
        bronnen = response.json()
        return render_template('bron_list.html', bronnen=bronnen)
    except Exception as e:
        flash(str(e), 'danger')
        return render_template('bron_list.html', bronnen=[])


@bronfrontend.route('/bronnen/<int:bron_id>/', methods=['GET', 'POST'])
def bron_detail(bron_id):
    if request.method == 'POST':
        data = {
            'naam': request.form.get('naam'),
            'beschrijving': request.form.get('beschrijving')
        }
        try:
            response = requests.put(f'{API_BASE_URL}{bron_id}/', json=data)
            if response.status_code == 404:
                raise BronNotFoundException('Bron niet gevonden.')
            elif response.status_code != 200:
                raise BronAPIException('Kon bron niet updaten.')
            flash('Bron succesvol bijgewerkt.', 'success')
            return redirect(url_for('bronfrontend.bron_detail', bron_id=bron_id))
        except Exception as e:
            flash(str(e), 'danger')

    try:
        response = requests.get(f'{API_BASE_URL}{bron_id}/')
        if response.status_code == 404:
            raise BronNotFoundException('Bron niet gevonden.')
        elif response.status_code != 200:
            raise BronAPIException('Kon brondetail niet ophalen.')
        bron = response.json()
        return render_template('bron_detail.html', bron=bron)
    except Exception as e:
        flash(str(e), 'danger')
        return render_template('bron_detail.html', bron=None)


@bronfrontend.route('/bronnen/nieuw/', methods=['GET', 'POST'])
def bron_create():
    if request.method == 'POST':
        data = {
            'naam': request.form.get('naam'),
            'beschrijving': request.form.get('beschrijving')
        }
        try:
            response = requests.post(API_BASE_URL, json=data)
            if response.status_code != 201:
                raise BronAPIException('Kon bron niet aanmaken.')
            bron = response.json()
            flash('Bron succesvol aangemaakt.', 'success')
            return redirect(url_for('bronfrontend.bron_detail', bron_id=bron['id']))
        except Exception as e:
            flash(str(e), 'danger')
    return render_template('bron_form.html', bron=None)