from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

from gandalhub.settings import LOGIN_REDIRECT_URL

class login:
    def __init__(self):
        pass

    def method(self, *args, **kwargs):
        raise NotImplementedError

# === AUTHENTIFICATION ===

from quiz.forms import CustomUserCreationForm, CustomAuthenticationForm

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('dashboard')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'front/account/login.html', {'form': form})

# views.py

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('index')
  # Redirige vers la page de connexion après déconnexion
    return redirect('index')  # Redirige vers une page par défaut si ce n'est pas une requête POST

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('account_login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'front/register.html', {'form': form})


from quiz.models import UserProfile

@login_required
def dashboard(request):
    profiles = UserProfile.objects.all()  # Récupère tous les profils avec photos
    return render(request, 'dashboard.html', {
        'profiles': profiles,
    })

from django.shortcuts import redirect, render

def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  # Redirige les utilisateurs connectés vers le tableau de bord
    return render(request, 'front/index.html')  # Affiche la page d'accueil pour les non-connectés


def about(request):
    return render(request, 'front/about.html')


def contact(request):
    return render(request, 'front/contact.html')


# === PAGES DES COURS ET ÉVÉNEMENTS ===
from quiz.models import Course, Quiz, Question

def course_details(request):
    return render(request, 'front/course_details.html')


def courses(request):
    courses = Course.objects.all()
    levels = ['Débutant', 'Intermédiaire', 'Avancé']
    courses_data = []

    for course in courses:
        quizzes_by_level = {level: [] for level in levels}
        for level in levels:
            quiz_ids = Question.objects.filter(course=course, quiz__level=level).values_list('quiz_id', flat=True).distinct()
            quizzes = Quiz.objects.filter(id__in=quiz_ids, level=level)
            quizzes_by_level[level] = list(quizzes)
        courses_data.append({
            'course': course,
            'quizzes_by_level': quizzes_by_level
        })

    return render(request, 'front/courses.html', {
        'courses_data': courses_data
    })


def events(request):
    return render(request, 'front/events.html')


# === PAGES SUPPLÉMENTAIRES ===
def pricing(request):
    return render(request, 'front/pricing.html')


def starter_page(request):
    return render(request, 'front/starter_page.html')


def trainers(request):
    return render(request, 'front/trainers.html')


# === GESTION DES MOTS DE PASSE ===
class CustomPasswordResetView(PasswordResetView):
    template_name = 'front/forgot_password.html'
    email_template_name = 'front/password_reset_email.html'
    success_url = '/reset_password_done/'


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'front/reset_password_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'front/reset_password_confirm.html'


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'front/reset_password_complete.html'


from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('account_login')  # Redirige après inscription
    else:
        form = UserCreationForm()
    return render(request, 'account/signup.html', {'form': form})


from django.shortcuts import redirect
from django.contrib import messages

def newsletter(request):
    if request.method == "POST":
        email = request.POST.get('email')
        # Ici tu peux enregistrer l'email ou envoyer un mail
        messages.success(request, "Merci pour votre inscription à la newsletter !")
        return redirect('contact')
    return redirect('contact')

