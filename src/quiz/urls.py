from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    # URLs pour les quiz
    path('list/', views.quiz_list, name='quiz_list'),
    path('progress/', views.user_progress, name='progress'),
    path('<int:quiz_id>/detail/', views.quiz_detail, name='quiz_detail'),
    path('<int:quiz_id>/start/', views.start_quiz, name='start_quiz'),
    path('<int:quiz_id>/submit/', views.submit_quiz, name='submit_quiz'),
]
