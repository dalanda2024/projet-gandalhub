from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), 
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('course_details/', views.course_details, name='course_details'),
    path('courses/', views.courses, name='courses'),
    path('events/', views.events, name='events'),
    path('pricing/', views.pricing, name='pricing'),
    path('trainers/', views.trainers, name='trainers'), 
    
]
