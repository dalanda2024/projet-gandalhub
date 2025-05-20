from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Quiz, UserQuizProgress, Course, UserProfile


def select_quiz(request):
    course_id = request.GET.get('course_id')
    level = request.GET.get('level')
    courses = Course.objects.all()
    quizzes = Quiz.objects.all()

    # Construction d'un mapping cours -> quiz par niveau
    course_quiz_map = []
    for course in courses:
        quizzes_by_level = {}
        for lvl in ['Débutant', 'Intermédiaire', 'Avancé']:
            quiz_ids = course.questions.filter(quiz__level=lvl).values_list('quiz_id', flat=True).distinct()
            quizzes_by_level[lvl] = Quiz.objects.filter(id__in=quiz_ids, level=lvl)
        course_quiz_map.append({
            'course': course,
            'quizzes_by_level': quizzes_by_level
        })

    # Filtrage selon sélection utilisateur
    if course_id:
        quizzes = quizzes.filter(questions__course__id=course_id).distinct()
    if level:
        quizzes = quizzes.filter(level=level)

    selected_course_obj = Course.objects.filter(id=course_id).first() if course_id else None

    return render(request, 'quiz/select_quiz.html', {
        'quizzes': quizzes,
        'courses': courses,
        'selected_course': int(course_id) if course_id else None,
        'selected_level': level,
        'levels': ['Débutant', 'Intermédiaire', 'Avancé'],
        'selected_course_obj': selected_course_obj,
        'course_quiz_map': course_quiz_map,
    })


def start_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    course_id = request.GET.get('course_id')
    
    if course_id:
        course = get_object_or_404(Course, id=course_id)
        questions = quiz.questions.filter(course=course)
    else:
        questions = quiz.questions.all()

    return render(request, 'quiz/start_quiz.html', {
        'quiz': quiz,
        'questions': questions,
        'selected_course': course if course_id else None
    })


@csrf_exempt
def submit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()
    score = 0
    total = questions.count()
    results = []

    # Calcul du score et collecte des résultats
    for question in questions:
        selected = request.POST.get(f"question_{question.id}")
        correct = question.choices.filter(is_correct=True).first()

        if selected == str(correct.id):
            score += 1
            results.append((question, True, correct.text, question.explanation, ""))
        else:
            selected_choice = question.choices.filter(id=selected).first()
            selected_text = selected_choice.text if selected_choice else "Aucune"
            results.append((question, False, correct.text, question.explanation, selected_text))

    # Enregistrer la progression de l'utilisateur si connecté
    if request.user.is_authenticated:
        UserQuizProgress.objects.create(
            user=request.user,
            quiz=quiz,
            score=score,
            total=total
        )

    # Calcul du pourcentage de score
    score_percent = (score / total) * 100

    # Système de recommandations basé sur le score
    if score_percent < 50:
        recommendation = f"Résultat insuffisant. Révisez le thème : {quiz.theme} (niveau : {quiz.level})."
    elif score_percent < 80:
        recommendation = f"Bon début ! Vous pourriez renforcer vos connaissances sur : {quiz.theme}."
    else:
        recommendation = "Excellent travail ! Vous pouvez passer au niveau supérieur."

    # Rendu de la page des résultats
    return render(request, 'quiz/result.html', {
        'score': score,
        'total': total,
        'quiz': quiz,
        'results': results,
        'recommendation': recommendation,
    })


@login_required
def user_progress(request):
    progress = UserQuizProgress.objects.filter(user=request.user).order_by('-completed_at')
    return render(request, 'quiz/progress.html', {'progress': progress})


@login_required
def dashboard(request):
    quizzes = Quiz.objects.all()[:5]  # Affiche les 5 premiers quiz
    progress = UserQuizProgress.objects.filter(user=request.user).order_by('-completed_at')[:5]  # Affiche les 5 derniers résultats
    profiles = UserProfile.objects.all()  # Récupère tous les profils avec photos
    return render(request, 'front/dashboard.html', {
        'quizzes': quizzes,
        'progress': progress,
        'profiles': profiles,
    })


def user_photos(request):
    profiles = UserProfile.objects.all()
    return render(request, 'quiz/user_photos.html', {'profiles': profiles})

