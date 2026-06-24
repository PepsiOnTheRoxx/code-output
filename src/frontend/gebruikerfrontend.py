from flask import Blueprint, render_template, request, redirect, url_for, flash
import requests
from src.frontend.gebruikerfrontend_exceptions import GebruikerAPIError

gebruiker_frontend = Blueprint("gebruiker_frontend", __name__, template_folder="templates")

API_BASE_URL = "http://localhost:8000/api/gebruiker"


@gebruiker_frontend.route("/gebruikers/")
def gebruikers_lijst():
    try:
        response = requests.get(API_BASE_URL)
        response.raise_for_status()
        gebruikers = response.json()
    except requests.RequestException as e:
        flash("Fout bij het ophalen van gebruikers.", "danger")
        gebruikers = []
    except GebruikerAPIError as exc:
        flash(str(exc), "danger")
        gebruikers = []
    return render_template("gebruiker_lijst.html", gebruikers=gebruikers)


@gebruiker_frontend.route("/gebruikers/<int:gebruiker_id>/")
def gebruiker_detail(gebruiker_id):
    try:
        response = requests.get(f"{API_BASE_URL}/{gebruiker_id}")
        response.raise_for_status()
        gebruiker = response.json()
    except requests.RequestException as e:
        flash("Fout bij het ophalen van gebruiker.", "danger")
        return redirect(url_for("gebruiker_frontend.gebruikers_lijst"))
    except GebruikerAPIError as exc:
        flash(str(exc), "danger")
        return redirect(url_for("gebruiker_frontend.gebruikers_lijst"))
    return render_template("gebruiker_detail.html", gebruiker=gebruiker)


@gebruiker_frontend.route("/gebruikers/nieuw/", methods=["GET", "POST"])
def gebruiker_nieuw():
    if request.method == "POST":
        data = {
            "naam": request.form.get("naam"),
            "email": request.form.get("email"),
        }
        try:
            response = requests.post(API_BASE_URL, json=data)
            response.raise_for_status()
            flash("Gebruiker succesvol aangemaakt.", "success")
            return redirect(url_for("gebruiker_frontend.gebruikers_lijst"))
        except requests.RequestException as e:
            flash("Fout bij het aanmaken van gebruiker.", "danger")
        except GebruikerAPIError as exc:
            flash(str(exc), "danger")
        return render_template("gebruiker_formulier.html", gebruiker=data)
    return render_template("gebruiker_formulier.html", gebruiker={})


@gebruiker_frontend.route("/gebruikers/<int:gebruiker_id>/bewerk/", methods=["GET", "POST"])
def gebruiker_bewerk(gebruiker_id):
    if request.method == "POST":
        data = {
            "naam": request.form.get("naam"),
            "email": request.form.get("email"),
        }
        try:
            response = requests.put(f"{API_BASE_URL}/{gebruiker_id}", json=data)
            response.raise_for_status()
            flash("Gebruiker succesvol bijgewerkt.", "success")
            return redirect(url_for("gebruiker_frontend.gebruikers_lijst"))
        except requests.RequestException as e:
            flash("Fout bij het bijwerken van gebruiker.", "danger")
        except GebruikerAPIError as exc:
            flash(str(exc), "danger")
        return render_template("gebruiker_formulier.html", gebruiker=data, edit=True)
    else:
        try:
            response = requests.get(f"{API_BASE_URL}/{gebruiker_id}")
            response.raise_for_status()
            gebruiker = response.json()
        except requests.RequestException as e:
            flash("Fout bij het ophalen van gebruiker.", "danger")
            return redirect(url_for("gebruiker_frontend.gebruikers_lijst"))
        except GebruikerAPIError as exc:
            flash(str(exc), "danger")
            return redirect(url_for("gebruiker_frontend.gebruikers_lijst"))
        return render_template("gebruiker_formulier.html", gebruiker=gebruiker, edit=True)


@gebruiker_frontend.route("/gebruikers/<int:gebruiker_id>/verwijder/", methods=["POST"])
def gebruiker_verwijder(gebruiker_id):
    try:
        response = requests.delete(f"{API_BASE_URL}/{gebruiker_id}")
        response.raise_for_status()
        flash("Gebruiker succesvol verwijderd.", "success")
    except requests.RequestException as e:
        flash("Fout bij het verwijderen van gebruiker.", "danger")
    except GebruikerAPIError as exc:
        flash(str(exc), "danger")
    return redirect(url_for("gebruiker_frontend.gebruikers_lijst"))