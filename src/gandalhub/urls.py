"""
URL configuration for gandalhub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('front.urls')),  # Inclure les URLs de l'application "front"
    #path('accounts/login/', LoginView.as_view(template_name='account/login.html'), name='account_login'),
    path('quiz/', include('quiz.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

