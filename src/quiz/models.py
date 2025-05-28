from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    quizzes = models.ManyToManyField('Quiz', related_name='courses', blank=True)

    def __str__(self):
        return self.title

class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(default="Pas de description disponible")
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE,
        null=True,  # Permettre temporairement null
        blank=True,
        default=None  # Valeur par défaut None
    )
    level = models.CharField(
        max_length=20,
        choices=[
            ('Débutant', 'Débutant'),
            ('Intermédiaire', 'Intermédiaire'),
            ('Avancé', 'Avancé'),
        ]
    )

    def __str__(self):
        return self.title
    
    def get_default_questions(self):
        javascript_questions = {
            'Débutant': [
                {
                    'text': 'Quelle est la syntaxe correcte pour déclarer une variable en JavaScript ?',
                    'choices': [
                        ('let maVariable = 10;', True),
                        ('variable maVariable = 10;', False),
                        ('val maVariable = 10;', False),
                    ]
                },
                {
                    'text': 'Comment afficher "Hello World" dans la console ?',
                    'choices': [
                        ('console.log("Hello World");', True),
                        ('print("Hello World");', False),
                        ('echo("Hello World");', False),
                    ]
                },
                {
                    'text': 'Quel est le type de données de : typeof(42) ?',
                    'choices': [
                        ('number', True),
                        ('integer', False),
                        ('string', False),
                    ]
                }
            ],
            'Intermédiaire': [
                {
                    'text': 'Quelle méthode permet de convertir un JSON en objet JavaScript ?',
                    'choices': [
                        ('JSON.parse()', True),
                        ('JSON.stringify()', False),
                        ('JSON.convert()', False),
                    ]
                }
            ]
        }
        return javascript_questions.get(self.level, [])

    def create_questions_by_level(self):
        questions_data = self.get_default_questions()
        for q_data in questions_data:
            question = Question.objects.create(
                quiz=self,
                text=q_data['text'],
                order=self.questions.count() + 1
            )
            for choice_text, is_correct in q_data['choices']:
                Choice.objects.create(
                    question=question,
                    text=choice_text,
                    is_correct=is_correct
                )

class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "User Progress"

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title}"
    
    @property
    def score_percent(self):
        return (self.score / self.quiz.questions.count()) * 100 if self.quiz.questions.count() > 0 else 0
    
    @property
    def level_status(self):
        score = self.score_percent
        if score >= 80:
            return 'Excellent'
        elif score >= 50:
            return 'En progression'
        return 'À améliorer'

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.quiz.title} - Question {self.order}"

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.question.text} - {self.text}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)  # Modification ici
    total_score = models.IntegerField(default=0)
    quizzes_completed = models.IntegerField(default=0)

    def __str__(self):
        return f"Profil de {self.user.username}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()