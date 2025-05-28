from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from front.models import Category, Course
from django.core.files import File
import os

class Command(BaseCommand):
    help = 'Create all courses with categories and instructors'

    def handle(self, *args, **kwargs):
        # 1. Création de toutes les catégories
        categories = [
            {'name': 'Cuisine', 'slug': 'cuisine'},
            {'name': 'Make Up', 'slug': 'makeup'},
            {'name': 'Couture', 'slug': 'couture'},
            {'name': 'Pâtisserie', 'slug': 'patisserie'},
            {'name': 'Informatique', 'slug': 'informatique'},
            {'name': 'Gestion Projet', 'slug': 'gestion-projet'},
            {'name': 'Réseau', 'slug': 'reseau'},
            {'name': 'Développement Personnel', 'slug': 'developpement-personnel'},
            {'name': 'Entreprenariat', 'slug': 'entreprenariat'},
        ]
        
        for cat_data in categories:
            Category.objects.get_or_create(**cat_data)
            self.stdout.write(f'Catégorie créée: {cat_data["name"]}')

        # 2. Création de tous les instructeurs
        instructors = [
            {'username': 'chef_aminata', 'first_name': 'Aminata', 'last_name': 'Diallo'},
            {'username': 'fatoumata_b', 'first_name': 'Fatoumata', 'last_name': 'B.'},
            {'username': 'mariam_d', 'first_name': 'Mariam', 'last_name': 'D.'},
            {'username': 'chef_oumar', 'first_name': 'Oumar', 'last_name': 'S.'},
            {'username': 'ibrahima_k', 'first_name': 'Ibrahima', 'last_name': 'K.'},
            {'username': 'aissatou_d', 'first_name': 'Aissatou', 'last_name': 'D.'},
            {'username': 'mohamed_c', 'first_name': 'Mohamed', 'last_name': 'C.'},
            {'username': 'mamadou_b', 'first_name': 'Mamadou', 'last_name': 'B.'},
            {'username': 'fatou_n', 'first_name': 'Fatou', 'last_name': 'N.'},
        ]
        
        for instr in instructors:
            User.objects.get_or_create(
                username=instr['username'],
                defaults={
                    'first_name': instr['first_name'],
                    'last_name': instr['last_name'],
                    'email': f"{instr['username']}@gandlhub.com",
                    'password': 'password123'
                }
            )
            self.stdout.write(f'Instructeur créé: {instr["first_name"]} {instr["last_name"]}')

        # 3. Création de tous les cours
        courses_data = [
            # Cuisine
            {
                'title': 'Cuisine Africaine Traditionnelle',
                'slug': 'cuisine-africaine-traditionnelle',
                'category_slug': 'cuisine',
                'instructor_username': 'chef_aminata',
                'description': 'Maîtrisez les plats emblématiques de la cuisine africaine avec nos chefs expérimentés.',
                'price': 99000,
                'static_image_path': 'CuisineAfricaineTraditionnelle.jpg',
                'students_count': 120,
                'likes_count': 89
            },
            
            # Make Up
            {
                'title': 'Maquillage Professionnel',
                'slug': 'maquillage-professionnel',
                'category_slug': 'makeup',
                'instructor_username': 'fatoumata_b',
                'description': 'Apprenez les techniques de maquillage pour toutes les occasions et types de peau.',
                'price': 75000,
                'static_image_path': 'MaquillageProfessionnel.jpg',
                'students_count': 95,
                'likes_count': 64
            },
            
            # Couture
            {
                'title': 'Couture Moderne Africaine',
                'slug': 'couture-moderne-africaine',
                'category_slug': 'couture',
                'instructor_username': 'mariam_d',
                'description': 'Créez des vêtements élégants inspirés des motifs traditionnels africains.',
                'price': 120000,
                'static_image_path': 'CoutureModerneAfricaine.jpg',
                'students_count': 78,
                'likes_count': 53
            },
            
            # Pâtisserie
            {
                'title': 'Pâtisserie Africaine',
                'slug': 'patisserie-africaine',
                'category_slug': 'patisserie',
                'instructor_username': 'chef_oumar',
                'description': 'Découvrez les secrets des desserts traditionnels africains et modernes.',
                'price': 85000,
                'static_image_path': 'PatisserieAfricaine.jpg',
                'students_count': 62,
                'likes_count': 47
            },
            
            # Informatique
            {
                'title': 'Bureautique Essentielle',
                'slug': 'bureautique-essentielle',
                'category_slug': 'informatique',
                'instructor_username': 'ibrahima_k',
                'description': 'Maîtrisez Word, Excel et PowerPoint pour le monde professionnel moderne.',
                'price': 150000,
                'static_image_path': 'BureautiqueEssentielle.jpg',
                'students_count': 135,
                'likes_count': 92
            },
            
            # Gestion Projet
            {
                'title': 'Gestion de Projet Agile',
                'slug': 'gestion-de-projet-agile',
                'category_slug': 'gestion-projet',
                'instructor_username': 'aissatou_d',
                'description': 'Méthodologies modernes pour mener à bien vos projets professionnels.',
                'price': 200000,
                'static_image_path': 'GestiondeProjetAgile.jpg',
                'students_count': 88,
                'likes_count': 76
            },
            
            # Réseau
            {
                'title': 'Réseaux Informatiques',
                'slug': 'reseaux-informatiques',
                'category_slug': 'reseau',
                'instructor_username': 'mohamed_c',
                'description': 'Apprenez à configurer et administrer des réseaux informatiques professionnels.',
                'price': 250000,
                'static_image_path': 'RéseauxInformatiques.jpg',
                'students_count': 72,
                'likes_count': 58
            },
            
            # Développement Personnel
            {
                'title': 'Développement Personnel',
                'slug': 'developpement-personnel',
                'category_slug': 'developpement-personnel',
                'instructor_username': 'mamadou_b',
                'description': 'Boostez votre confiance en soi et améliorez vos compétences relationnelles.',
                'price': 80000,
                'static_image_path': 'DéveloppementPersonnel.jpg',
                'students_count': 105,
                'likes_count': 89
            },
            
            # Entreprenariat
            {
                'title': 'Lancez Votre Startup',
                'slug': 'lancez-votre-startup',
                'category_slug': 'entreprenariat',
                'instructor_username': 'fatou_n',
                'description': 'De l\'idée à la réalisation, toutes les étapes pour créer votre entreprise.',
                'price': 180000,
                'static_image_path': 'Entreprenariat.jpg',
                'students_count': 142,
                'likes_count': 97
            }
        ]
        
        for course_data in courses_data:
            category = Category.objects.get(slug=course_data['category_slug'])
            instructor = User.objects.get(username=course_data['instructor_username'])
            
            course = Course.objects.create(
                title=course_data['title'],
                slug=course_data['slug'],
                category=category,
                instructor=instructor,
                description=course_data['description'],
                price=course_data['price'],
                static_image_path=course_data['static_image_path']
            )
            
            # Simuler les étudiants (simplifié pour la démo)
            for i in range(min(course_data['students_count'], 10)):  # Limité à 10 pour la démo
                course.students.add(User.objects.create_user(
                    username=f'student_{course.slug}_{i}',
                    password='password123'
                ))
            
            self.stdout.write(self.style.SUCCESS(f'Cours créé: {course.title}'))

        self.stdout.write(self.style.SUCCESS('Tous les cours ont été créés avec succès!'))