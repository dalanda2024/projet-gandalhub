from django.urls import path, include
from . import views
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

urlpatterns = [
    # === Pages principales ===
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    # === Authentification ===
    path('login/', views.login_view, name='account_login'),
    path('logout/', views.logout_view, name='account_logout'),
    path('register/', views.register_view, name='account_signup'),
    
    # === Profil utilisateur et Tableau de bord ===
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # === Cours et événements ===
    path('courses/', views.courses, name='courses'),
    path('course/<slug:slug>/', views.course_detail, name='course_detail'),
    path('trainers/', views.trainers, name='trainers'),
    path('events/', views.events, name='events'),
    path('pricing/', views.pricing, name='pricing'),
    
    # === Newsletter ===
    path('newsletter/', views.newsletter, name='newsletter'),
    
    # === Réinitialisation du mot de passe ===
    path('reset_password/', 
        views.CustomPasswordResetView.as_view(), 
        name='password_reset'),
    path('reset_password_done/', 
        views.CustomPasswordResetDoneView.as_view(), 
        name='password_reset_done'),
    path('reset_password_confirm/<uidb64>/<token>/', 
        views.CustomPasswordResetConfirmView.as_view(), 
        name='password_reset_confirm'),
    path('reset_password_complete/', 
        views.CustomPasswordResetCompleteView.as_view(), 
        name='password_reset_complete'),
    
    # === Django Allauth ===
    path('accounts/', include('allauth.urls')),
]
