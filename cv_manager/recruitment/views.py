from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CVForm
from django.contrib.auth.decorators import login_required

from django.contrib.auth import login, authenticate
from .forms import RegisterForm
from django.contrib import messages
from .models import CV
# cv_manager/views.py
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import render
from django.contrib import admin
from django.db.models import Q
from .utils import send_notification_email, get_admin_emails

import zipfile
from django.http import HttpResponse
import os
from django.contrib.auth.decorators import user_passes_test

def home(request):
    return render(request, 'home.html')  # Si vous avez un template 'home.html'


@login_required
def add_cv(request):
    if request.method == 'POST':
        form = CVForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user  # Associer le CV à l'utilisateur connecté
            form.save()
            return redirect('home')
    else:
        form = CVForm()
    return render(request, 'add_cv.html', {'form': form})

@login_required
def upload_cv(request):
    if request.method == 'POST':
        form = CVForm(request.POST, request.FILES)
        if form.is_valid():
            cv = form.save(commit=False)
            cv.user = request.user  # Associer le CV à l'utilisateur connecté
            cv.save()
            return redirect('cv_list')  # Rediriger vers la liste des CVs
    else:
        form = CVForm()
    return render(request, 'upload_cv.html', {'form': form})



def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Sauvegarder l'utilisateur
            user.set_password(form.cleaned_data['password'])  # Crypter le mot de passe
            user.save()
            # Authentifier et connecter l'utilisateur immédiatement après l'inscription
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                messages.success(request, "Inscription réussie ! Bienvenue.")
                return redirect('home')  # Rediriger vers la page d'accueil après l'inscription
        else:
            messages.error(request, "Une erreur est survenue. Veuillez réessayer.")
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})

# def profile(request):
#     return render(request, 'profile.html')
@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})

# def cv_list(request):
#     # Code pour récupérer et afficher la liste des CV
#     return render(request, 'cv_list.html')

# def cv_list(request):
#     cvs = CV.objects.all()
#     if not cvs:
#         message = "No CVs uploaded yet."
#     else:
#         message = None
#     return render(request, 'cv_list.html', {'cvs': cvs, 'message': message})

# def cv_list(request):
#     cvs = CV.objects.all()
#     for cv in cvs:
#         try:
#             if cv.cv_file and not cv.cv_file.url:
#                 cv.cv_file = None
#         except ValueError:
#             cv.cv_file = None  # Si une exception se produit, on assigne None
#     return render(request, "cv_list.html", {"cvs": cvs})
# def cv_list(request):
#     cvs = CV.objects.all()
#
#     for cv in cvs:
#         try:
#             # Vérifier si le fichier 'cv_file' existe et est valide
#             if cv.cv_file:
#                 # Vérifier si l'URL du fichier est disponible (cela évite une exception si 'cv_file' est un champ vide)
#                 if not cv.cv_file.url:
#                     cv.cv_file = None  # Si l'URL n'est pas disponible, on réinitialise le champ à None
#         except ValueError:
#             # Si une exception se produit (par exemple, si 'cv_file' est mal configuré), on assigne None
#             cv.cv_file = None
#
#     return render(request, "cv_list.html", {"cvs": cvs})

# @login_required
# def cv_list(request):
#     # Filtrer les CVs par l'utilisateur connecté
#     cvs = CV.objects.filter(user=request.user)

@login_required
def cv_list(request):
    # Vérifier si l'utilisateur est un administrateur
    if request.user.is_staff:
        # Si l'utilisateur est administrateur, afficher tous les CVs
        cvs = CV.objects.all()
    else:
        # Sinon, afficher seulement les CVs de l'utilisateur connecté
        cvs = CV.objects.filter(user=request.user)

    return render(request, 'cv_list.html', {'cvs': cvs})

    return render(request, 'cv_list.html', {'cvs': cvs})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Inscription réussie!")
            return redirect('cv_list')  # Rediriger vers la page des CVs
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

# Vue pour la connexion d'un utilisateur
def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Bienvenue ! Vous êtes connecté.")
            return redirect('cv_list')  # Rediriger vers la page des CVs
        else:
            messages.error(request, "Identifiants incorrects.")
    else:
        form = AuthenticationForm()
    return render(request, 'signin.html', {'form': form})

# Vue pour la déconnexion d'un utilisateur
@login_required
def signout(request):
    logout(request)
    messages.info(request, "Vous êtes déconnecté.")
    return redirect('home')  # Rediriger vers la page des CVs

@admin.register(CV)
class CVAdmin(admin.ModelAdmin):
    list_display = ('user', 'cv_file', 'created_at')  # Ajuste selon les champs du modèle
    search_fields = ('user__username',)

# @login_required
# def search_cvs(request):
#     query = request.GET.get('q', '')  # Mot-clé
#     user_filter = request.GET.get('user', '')  # Nom d'utilisateur
#     date_from = request.GET.get('date_from', '')  # Date de début
#     date_to = request.GET.get('date_to', '')  # Date de fin
#
#     cvs = CV.objects.all()
#
#     if query:
#         cvs = cvs.filter(Q(title__icontains=query) | Q(user__username__icontains=query))
#     if user_filter:
#         cvs = cvs.filter(user__username=user_filter)
#     if date_from:
#         cvs = cvs.filter(date_uploaded__gte=date_from)
#     if date_to:
#         cvs = cvs.filter(date_uploaded__lte=date_to)
#
#     return render(request, 'cv_search.html', {'cvs': cvs})
@login_required
def search_cvs(request):
    query = request.GET.get('q', '')  # Mot-clé
    user_filter = request.GET.get('user', '')  # Nom d'utilisateur (administrateur uniquement)
    date_from = request.GET.get('date_from', '')  # Date de début
    date_to = request.GET.get('date_to', '')  # Date de fin

    # Si l'utilisateur est un administrateur, il peut voir tous les CV
    if request.user.is_superuser:
        cvs = CV.objects.all()
    else:  # Sinon, il ne voit que ses propres CV
        cvs = CV.objects.filter(user=request.user)

    # Appliquer les filtres
    if query:
        cvs = cvs.filter(Q(title__icontains=query) | Q(user__username__icontains=query))
    if user_filter and request.user.is_superuser:  # Seul un administrateur peut filtrer par utilisateur
        cvs = cvs.filter(user__username=user_filter)
    if date_from:
        cvs = cvs.filter(date_uploaded__gte=date_from)
    if date_to:
        cvs = cvs.filter(date_uploaded__lte=date_to)

    return render(request, 'cv_search.html', {'cvs': cvs})

@login_required
def edit_cv(request, cv_id):
    cv = get_object_or_404(CV, id=cv_id)

    # Vérification des permissions
    if not request.user.is_superuser and cv.user != request.user:
        messages.error(request, "Vous n'êtes pas autorisé à modifier ce CV.")
        return redirect('cv_list')

    if request.method == 'POST':
        form = CVForm(request.POST, request.FILES, instance=cv)
        if form.is_valid():
            form.save()
            admin_emails = get_admin_emails()
        if admin_emails:
            send_notification_email(
                subject="CV modifié",
                message=f"Le CV de {cv.user.username} a été modifié.",
                recipient_list=admin_emails
            )

            messages.success(request, "CV modifié avec succès.")

            return redirect('cv_list')
    else:
        form = CVForm(instance=cv)

    return render(request, 'edit_cv.html', {'form': form})


# @login_required
# def delete_cv(request, cv_id):
#     cv = get_object_or_404(CV, id=cv_id)
#
#     # Vérification des permissions
#     if not request.user.is_superuser and cv.user != request.user:
#         return HttpResponseForbidden("Vous n'êtes pas autorisé à supprimer ce CV.")
#
#     if request.method == 'POST':
#         cv.delete()
#         messages.success(request, "CV supprimé avec succès.")
#         return redirect('cv_list')
#
#     return render(request, 'confirm_delete_cv.html', {'cv': cv})

@login_required
def delete_cv(request, cv_id):
    cv = get_object_or_404(CV, id=cv_id)
    if request.user == cv.user or request.user.is_staff:
        cv.delete()

        admin_emails = get_admin_emails()
        if admin_emails:
            send_notification_email(
                subject="CV supprimé",
                message=f"Le CV de {cv.user.username} a été supprimé.",
                recipient_list=admin_emails
            )
        messages.success(request, "CV supprimé avec succès.")

    else:
        messages.error(request, "Vous n'avez pas la permission de supprimer ce CV.")
    return redirect("cv_list")



def is_admin(user):
    return user.is_superuser

# Vue qui génère et permet de télécharger tous les CVs dans un fichier zip
@user_passes_test(is_admin)  # Cette ligne restreint l'accès aux admins uniquement
def download_all_cvs(request):
    # Récupérer tous les CVs dans la base de données
    cvs = CV.objects.all()

    # Créer un fichier zip en mémoire
    zip_filename = "all_cvs.zip"
    response = HttpResponse(content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename={zip_filename}'

    # Créer le fichier zip dans la réponse
    with zipfile.ZipFile(response, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for cv in cvs:
            # Vérifier si le CV a un fichier attaché
            if cv.cv_file:
                # Récupérer le chemin du fichier CV
                file_path = cv.cv_file.path

                # Ajouter le fichier au zip
                zip_file.write(file_path, os.path.basename(file_path))

    return response


