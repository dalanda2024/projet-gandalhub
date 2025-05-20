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
    path('newsletter/', views.newsletter, name='newsletter'),
    



    # === Pages des cours et événements ===
    path('course_details/', views.course_details, name='course_details'),
    path('courses/', views.courses, name='courses'),
    path('events/', views.events, name='events'),

    # === Pages supplémentaires ===
    path('pricing/', views.pricing, name='pricing'),
    path('starter_page/', views.starter_page, name='starter_page'),
    path('trainers/', views.trainers, name='trainers'),

    # === Authentification ===
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('forgot_password/', views.CustomPasswordResetView.as_view(), name='forgot_password'),
    path('reset_password_done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('accounts/', include('allauth.urls')),

    # === Django Allauth ===
    path('dashboard/', views.dashboard, name='dashboard'),  # Définition de l'URL pour le tableau de bord
]
