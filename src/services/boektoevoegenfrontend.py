from django.shortcuts import render, redirect
from django.urls import reverse
from src.services.boektoevoegenfrontend_exceptions import BoekToevoegenFout
from .models import Boek
from .forms import BoekForm

def boek_toevoegen_view(request):
    if request.method == 'POST':
        form = BoekForm(request.POST)
        if form.is_valid():
            try:
                boek = form.save()
                return redirect(reverse('boek_detail', args=[boek.id]))
            except Exception as exc:
                raise BoekToevoegenFout("Kon boek niet toevoegen") from exc
    else:
        form = BoekForm()
    return render(request, 'boek_toevoegen.html', {'form': form})