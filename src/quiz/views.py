from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Quiz, UserProgress, Course, UserProfile, Question, Choice  # Ajout de Question et Choice
import random


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


def get_course_questions(course_name, level):
    questions_bank = {
        'Python pour débutants': {
            'Débutant': [
                {
                    'text': 'Quelle est la syntaxe correcte pour effectuer une addition en Python ?',
                    'choices': [
                        ('a + b', True),
                        ('a.add(b)', False),
                        ('add(a, b)', False),
                    ]
                },
                {
                    'text': 'Comment déclarer une chaîne de caractères en Python ?',
                    'choices': [
                        ('texte = "Hello"', True),
                        ('string texte = "Hello"', False),
                        ('let texte = "Hello"', False),
                    ]
                },
                {
                    'text': 'Quelle est la fonction pour obtenir la longueur d\'une liste ?',
                    'choices': [
                        ('len(liste)', True),
                        ('liste.size()', False),
                        ('liste.length', False),
                    ]
                },
                {
                    'text': 'Comment commenter une ligne en Python ?',
                    'choices': [
                        ('# Commentaire', True),
                        ('// Commentaire', False),
                        ('/* Commentaire */', False),
                    ]
                }
            ],
            'Intermédiaire': [
                {
                    'text': 'Quelle est la différence entre une liste et un tuple ?',
                    'choices': [
                        ('Les tuples sont immuables, les listes sont mutables', True),
                        ('Les tuples sont plus rapides', False),
                        ('Il n\'y a pas de différence', False),
                    ]
                },
                {
                    'text': 'Comment gérer les exceptions en Python ?',
                    'choices': [
                        ('try/except', True),
                        ('if/else', False),
                        ('switch/case', False),
                    ]
                },
                {
                    'text': 'Qu\'est-ce qu\'un générateur en Python ?',
                    'choices': [
                        ('Une fonction qui utilise yield', True),
                        ('Une classe spéciale', False),
                        ('Un type de boucle', False),
                    ]
                }
            ],
            'Avancé': [
                {
                    'text': 'Expliquez le fonctionnement des métaclasses en Python',
                    'choices': [
                        ('Une classe qui définit le comportement d\'autres classes', True),
                        ('Une classe abstraite', False),
                        ('Une classe statique', False),
                    ]
                },
                {
                    'text': 'Quelle est l\'utilité du décorateur @contextmanager ?',
                    'choices': [
                        ('Gérer les ressources dans un bloc with', True),
                        ('Gérer les exceptions', False),
                        ('Créer des itérateurs', False),
                    ]
                },
                {
                    'text': 'Comment fonctionne le Garbage Collector en Python ?',
                    'choices': [
                        ('Par comptage de références et détection de cycles', True),
                        ('Par libération manuelle de la mémoire', False),
                        ('Par nettoyage périodique automatique', False),
                    ]
                },
                {
                    'text': 'Comment fonctionne le GIL en Python ?',
                    'choices': [
                        ('Il permet un seul thread Python à la fois', True),
                        ('Il gère la mémoire', False),
                        ('Il optimise le code', False),
                    ]
                },
                {
                    'text': 'Qu\'est-ce que asyncio ?',
                    'choices': [
                        ('Un framework pour la programmation asynchrone', True),
                        ('Une bibliothèque de test', False),
                        ('Un gestionnaire de paquets', False),
                    ]
                }
            ]
        },
        'JavaScript Fondamentaux': {
            'Débutant': [
                {
                    'text': 'Comment déclarer une constante en JavaScript ?',
                    'choices': [
                        ('const x = 5;', True),
                        ('let x = 5;', False),
                        ('var x = 5;', False),
                    ]
                },
                {
                    'text': 'Quel est le résultat de typeof([]) ?',
                    'choices': [
                        ('object', True),
                        ('array', False),
                        ('list', False),
                    ]
                },
                {
                    'text': 'Comment déclarer une fonction en JavaScript ?',
                    'choices': [
                        ('function maFonction() {}', True),
                        ('def maFonction():', False),
                        ('void maFonction()', False),
                    ]
                },
                {
                    'text': 'Quelle méthode permet de sélectionner un élément HTML par son ID ?',
                    'choices': [
                        ('document.getElementById()', True),
                        ('document.querySelector()', False),
                        ('document.getElement()', False),
                    ]
                }
            ],
            'Avancé': [
                {
                    'text': 'Qu\'est-ce que le "Event Loop" en JavaScript ?',
                    'choices': [
                        ('Un mécanisme de gestion des tâches asynchrones', True),
                        ('Une boucle while infinie', False),
                        ('Un gestionnaire d\'événements DOM', False),
                    ]
                },
                {
                    'text': 'Expliquez le concept de "Closure" en JavaScript',
                    'choices': [
                        ('Une fonction qui conserve l\'accès à son scope parent', True),
                        ('Une fonction qui se ferme automatiquement', False),
                        ('Une fonction privée', False),
                    ]
                },
                {
                    'text': 'Qu\'est-ce que le "Prototype Chain" ?',
                    'choices': [
                        ('Le mécanisme d\'héritage en JavaScript', True),
                        ('Une liste chaînée de fonctions', False),
                        ('Un pattern de conception', False),
                    ]
                }
            ]
        }
    }
    
    # Augmentation du nombre de questions retournées
    questions = questions_bank.get(course_name, {}).get(level, [])
    return random.sample(questions, min(len(questions), 10))  # Retourne jusqu'à 10 questions

@login_required
def start_quiz(request, quiz_id):
    try:
        quiz = get_object_or_404(Quiz, id=quiz_id)
        
        # Vérifier si le quiz a un cours associé
        if not quiz.course:
            messages.error(request, "Ce quiz n'est associé à aucun cours.")
            return redirect('quiz:quiz_list')
            
        # Créer des questions si nécessaire
        if quiz.questions.count() == 0:
            course_title = quiz.course.title
            if 'Python' in course_title:
                create_python_questions(quiz)
            elif 'JavaScript' in course_title:
                create_javascript_questions(quiz)
            else:
                create_default_questions(quiz)

        questions = quiz.questions.prefetch_related('choices').all()
        
        if not questions.exists():
            messages.warning(request, "Ce quiz n'a pas encore de questions.")
            return redirect('quiz:quiz_list')

        context = {
            'quiz': quiz,
            'questions': questions,
            'total_questions': questions.count()
        }
        
        return render(request, 'quiz/start_quiz.html', context)
        
    except Exception as e:
        messages.error(request, f"Une erreur s'est produite : {str(e)}")
        return redirect('quiz:quiz_list')


@login_required
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
            results.append((question, True, correct.text, "", ""))
        else:
            selected_choice = question.choices.filter(id=selected).first()
            selected_text = selected_choice.text if selected_choice else "Aucune réponse"
            results.append((question, False, correct.text, "", selected_text))

    # Enregistrer la progression
    UserProgress.objects.create(
        user=request.user,
        quiz=quiz,
        score=score,
        completed=True
    )

    return render(request, 'quiz/result.html', {
        'quiz': quiz,
        'score': score,
        'total': total,
        'results': results,
    })


@login_required
def user_progress(request):
    # Récupérer tous les progrès de l'utilisateur
    progress = UserProgress.objects.filter(
        user=request.user,
        completed=True
    ).select_related('quiz').order_by('-completed_at')

    # Calculer les statistiques
    total_quizzes = Quiz.objects.count()
    total_completed = progress.count()

    context = {
        'progress': progress,
        'total_quizzes': total_quizzes,
        'total_completed': total_completed,
    }
    
    return render(request, 'quiz/progress.html', context)


@login_required
def dashboard(request):
    quizzes = Quiz.objects.all()[:5]  # Affiche les 5 premiers quiz
    progress = UserProgress.objects.filter(user=request.user).order_by('-completed_at')[:5]  # Affiche les 5 derniers résultats
    profiles = UserProfile.objects.all()  # Récupère tous les profils avec photos
    return render(request, 'front/dashboard.html', {
        'quizzes': quizzes,
        'progress': progress,
        'profiles': profiles,
    })


def user_photos(request):
    profiles = UserProfile.objects.all()
    return render(request, 'quiz/user_photos.html', {'profiles': profiles})


@login_required
def quiz_list(request):
    print("Démarrage de quiz_list")
    
    # Vérifier et créer des quiz pour chaque cours
    courses = Course.objects.all()
    for course in courses:
        if not Quiz.objects.filter(course=course).exists():
            print(f"Création des quiz par défaut pour le cours: {course.title}")
            # Créer un quiz pour chaque niveau
            for level in ['Débutant', 'Intermédiaire', 'Avancé']:
                Quiz.objects.create(
                    title=f"Quiz {level} - {course.title}",
                    description=f"Quiz de niveau {level} pour le cours {course.title}",
                    course=course,
                    level=level
                )
    
    # Récupération des données avec les quiz
    courses = Course.objects.prefetch_related('quiz_set').all()
    print(f"Nombre de cours trouvés: {courses.count()}")
    
    for course in courses:
        quizzes = course.quiz_set.all()
        print(f"Cours: {course.title} - Nombre de quiz: {quizzes.count()}")
        for quiz in quizzes:
            print(f"  - Quiz: {quiz.title} ({quiz.level})")

    context = {
        'courses': courses,
        'levels': ['Débutant', 'Intermédiaire', 'Avancé']
    }
    
    return render(request, 'quiz/quiz_list.html', context)


@login_required
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    return render(request, 'quiz/quiz_detail.html', {
        'quiz': quiz,
        'questions': quiz.questions.all()
    })


def create_python_questions(quiz):
    questions_data = [
        {
            'text': 'Quelle est la syntaxe pour une boucle for en Python ?',
            'choices': [
                ('for item in items:', True),
                ('for(i=0; i<10; i++)', False),
                ('foreach(item in items)', False),
            ]
        },
        {
            'text': 'Comment définir une fonction en Python ?',
            'choices': [
                ('def ma_fonction():', True),
                ('function ma_fonction()', False),
                ('void ma_fonction()', False),
            ]
        }
    ]
    create_quiz_questions(quiz, questions_data)

def create_javascript_questions(quiz):
    questions_data = [
        {
            'text': 'Comment déclarer une variable en JavaScript ?',
            'choices': [
                ('let maVariable = 10;', True),
                ('var maVariable = 10;', False),
                ('const maVariable = 10;', False),
            ]
        },
        {
            'text': 'Quelle méthode permet d\'ajouter un élément à un tableau ?',
            'choices': [
                ('push()', True),
                ('append()', False),
                ('add()', False),
            ]
        }
    ]
    create_quiz_questions(quiz, questions_data)

def create_quiz_questions(quiz, questions_data):
    for i, q_data in enumerate(questions_data, 1):
        question = Question.objects.create(
            quiz=quiz,
            text=q_data['text'],
            order=i
        )
        for choice_text, is_correct in q_data['choices']:
            Choice.objects.create(
                question=question,
                text=choice_text,
                is_correct=is_correct
            )

def create_default_questions(quiz):
    default_questions = [
        {
            'text': 'Question par défaut 1',
            'choices': [
                ('Réponse A', True),
                ('Réponse B', False),
                ('Réponse C', False),
            ]
        },
        {
            'text': 'Question par défaut 2',
            'choices': [
                ('Réponse 1', True),
                ('Réponse 2', False),
                ('Réponse 3', False),
            ]
        }
    ]
    
    for q_data in default_questions:
        question = Question.objects.create(
            quiz=quiz,
            text=q_data['text'],
            order=quiz.questions.count() + 1
        )
        for choice_text, is_correct in q_data['choices']:
            Choice.objects.create(
                question=question,
                text=choice_text,
                is_correct=is_correct
            )

