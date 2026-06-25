from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.services.boekaanpassenfrontend_exceptions import BoekNietGevondenException, BoekAanpassenValidatieException
from src.models import Boek
from src.database import db

boekaanpassen_blueprint = Blueprint('boekaanpassen', __name__)

@boekaanpassen_blueprint.route('/boeken/<int:boek_id>/aanpassen', methods=['GET', 'POST'])
def boek_aanpassen(boek_id):
    boek = Boek.query.get(boek_id)
    if not boek:
        raise BoekNietGevondenException(f"Boek met id {boek_id} niet gevonden.")

    if request.method == 'POST':
        titel = request.form.get('titel', '').strip()
        auteur = request.form.get('auteur', '').strip()
        isbn = request.form.get('isbn', '').strip()
        publicatiejaar = request.form.get('publicatiejaar', '').strip()

        if not titel or not auteur or not isbn or not publicatiejaar:
            flash('Alle velden zijn verplicht.', 'danger')
            raise BoekAanpassenValidatieException('Ingevulde data is ongeldig.')

        boek.titel = titel
        boek.auteur = auteur
        boek.isbn = isbn
        boek.publicatiejaar = publicatiejaar

        db.session.commit()
        return redirect(url_for('boekdetail.boek_detail', boek_id=boek.id))

    return render_template('BoekAanpassenTemplate.html', boek=boek)