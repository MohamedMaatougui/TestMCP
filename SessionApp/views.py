from django.shortcuts import render

# Create your views here.
# SessionApp/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Session
from .forms import SessionForm
from django.contrib import messages

# Liste des sessions
def session_list(request):
    sessions = Session.objects.all().order_by('-created_at')
    return render(request, 'SessionApp/session_list.html', {'sessions': sessions})

# Détails d'une session
def session_detail(request, pk):
    session = get_object_or_404(Session, pk=pk)
    return render(request, 'SessionApp/session_detail.html', {'session': session})

# Créer une session
def session_create(request):
    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Session créée avec succès.")
            return redirect('session_list')
    else:
        form = SessionForm()
    return render(request, 'SessionApp/session_form.html', {'form': form, 'title': 'Créer une session'})

# Mettre à jour une session
def session_update(request, pk):
    session = get_object_or_404(Session, pk=pk)
    if request.method == 'POST':
        form = SessionForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            messages.success(request, "Session mise à jour avec succès.")
            return redirect('session_list')
    else:
        form = SessionForm(instance=session)
    return render(request, 'SessionApp/session_form.html', {'form': form, 'title': 'Modifier la session'})

# Supprimer une session
def session_delete(request, pk):
    session = get_object_or_404(Session, pk=pk)
    if request.method == 'POST':
        session.delete()
        messages.success(request, "Session supprimée avec succès.")
        return redirect('session_list')
    return render(request, 'SessionApp/session_confirm_delete.html', {'session': session})
