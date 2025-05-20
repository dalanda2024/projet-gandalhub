from django.urls import path
from . import views
from .views import user_photos

urlpatterns = [
    path('', views.select_quiz, name='select_quiz'),
    path('<int:quiz_id>/', views.start_quiz, name='start_quiz'),
    path('<int:quiz_id>/submit/', views.submit_quiz, name='submit_quiz'),
    path('progress/', views.user_progress, name='user_progress'),
    path('front/dashboard/', views.dashboard, name='dashboard'),
    path('user-photos/', user_photos, name='user_photos'),
]
