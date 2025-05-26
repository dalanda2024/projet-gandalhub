from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    # Liste des cours
    path('courses/', views.courses, name='courses'),
    
    # Détail d'un cours (doit venir APRÈS les URLs spécifiques)
    path('courses/<slug:slug>/', views.course_detail, name='course_detail'),
    
    path('events/', views.events, name='events'),
    path('pricing/', views.pricing, name='pricing'),
    path('trainers/', views.trainers, name='trainers'),
]