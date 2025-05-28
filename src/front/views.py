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
    if request.user.is_authenticated:
        return redirect('index')  # Redirige vers le dashboard si déjà connecté
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            next_url = request.GET.get('next')
            return redirect(next_url if next_url else 'dashboard')  # Redirige vers le dashboard après connexion
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
    return render(request, 'front/dashboard.html', {
        'profiles': profiles,
    })

from django.shortcuts import redirect, render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from .models import Course, Category

def courses(request):
    courses = Course.objects.all().select_related('category', 'instructor')
    categories = Category.objects.all()
    return render(request, 'front/course_list.html', {
        'courses': courses,
        'categories': categories
    })

def course_detail(request, slug):
    course = get_object_or_404(Course.objects.prefetch_related('modules', 'resources'), slug=slug)
    context = {
        'course': course,
    }
    return render(request, 'front/course_detail.html', context)


def index(request):
    # Suppression de la redirection en boucle
    return render(request, 'front/index.html')

def about(request):
    return render(request, 'front/about.html')


def contact(request):
    return render(request, 'front/contact.html')


# === PAGES DES COURS ET ÉVÉNEMENTS ===
from quiz.models import Course, Quiz, Question

def course_details(request):
    return render(request, 'front/course_details.html')
# def course_details(request):
#     return render(request, 'front/course_details.html')


def courses(request):
    courses = Course.objects.prefetch_related('quizzes').all()
    levels = ['Débutant', 'Intermédiaire', 'Avancé']
    
    context = {
        'courses': courses,
        'levels': levels
    }
    
    return render(request, 'front/courses.html', context)
# def courses(request):
#     return render(request, 'front/courses.html')


@login_required
def events(request):
    return render(request, 'front/events.html')


# === PAGES SUPPLÉMENTAIRES ===
@login_required
def pricing(request):
    return render(request, 'front/pricing.html')


def starter_page(request):
    return render(request, 'front/starter_page.html')


@login_required
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

from django.db.models import Avg
from quiz.models import UserProgress, Quiz

@login_required
def profile_view(request):
    # Calcul des statistiques
    user_stats = {
        'quizzes_completed': UserProgress.objects.filter(user=request.user, completed=True).count(),
        'average_score': UserProgress.objects.filter(user=request.user).aggregate(Avg('score'))['score__avg'] or 0,
        'total_time': UserProgress.objects.filter(user=request.user).count() * 0.5  # Estimation: 30min par quiz
    }

    # Progression par niveau
    user_progress = {}
    for level in ['Débutant', 'Intermédiaire', 'Avancé']:
        level_stats = UserProgress.objects.filter(
            user=request.user,
            quiz__level=level,
            completed=True
        )
        user_progress[level] = {
            'completed': level_stats.count(),
            'score': level_stats.aggregate(Avg('score'))['score__avg'] or 0
        }

    # Recommandations basées sur les performances
    recommendations = []
    for level, stats in user_progress.items():
        if stats['score'] < 50:
            quiz = Quiz.objects.filter(level=level).first()
            recommendations.append({
                'title': f'Renforcer vos bases en {level}',
                'description': 'Votre score moyen est inférieur à 50%. Nous vous recommandons de revoir les concepts de base.',
                'quiz': quiz
            })
        elif stats['score'] < 80:
            quiz = Quiz.objects.filter(level=level).first()
            recommendations.append({
                'title': f'Améliorer votre niveau {level}',
                'description': 'Vous maîtrisez les bases. Continuez pour atteindre l\'excellence !',
                'quiz': quiz
            })

    # Derniers quiz complétés
    recent_quizzes = UserProgress.objects.filter(
        user=request.user,
        completed=True
    ).select_related('quiz').order_by('-completed_at')[:5]

    context = {
        'user': request.user,
        'stats': user_stats,
        'user_progress': user_progress,
        'recommendations': recommendations,
        'recent_quizzes': recent_quizzes,
    }
    
    return render(request, 'front/account/profile.html', context)

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserProfileForm

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre profil a été mis à jour avec succès.')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user.userprofile)
    
    return render(request, 'front/account/edit_profile.html', {'form': form})




def valider_paiement(request):
    if request.method == 'POST':
        mode = request.POST.get('mode_paiement')

        if mode == 'orange':
            phone = request.POST.get('orange_phone')
            code = request.POST.get('orange_code')
            # Traitement Orange Money
        elif mode == 'mtn':
            phone = request.POST.get('mtn_phone')
            code = request.POST.get('mtn_code')
            # Traitement MTN Money
        elif mode == 'card':
            number = request.POST.get('card_number')
            name = request.POST.get('card_name')
            expiry = request.POST.get('card_expiry')
            cvv = request.POST.get('card_cvv')
            # Traitement Carte Bancaire

        # Logique commune après paiement
        return redirect('confirmation_paiement')
