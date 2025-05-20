from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from quiz.models import UserProfile

class Command(BaseCommand):
    help = 'Créer des profils pour les utilisateurs existants sans profil.'

    def handle(self, *args, **kwargs):
        users_without_profiles = User.objects.filter(profile__isnull=True)
        for user in users_without_profiles:
            UserProfile.objects.create(user=user)
            self.stdout.write(self.style.SUCCESS(f'Profil créé pour l\'utilisateur : {user.username}'))
        self.stdout.write(self.style.SUCCESS('Tous les profils manquants ont été créés.'))