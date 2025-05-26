from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.urls import reverse
import os

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Slug")
    icon = models.CharField(
        max_length=50, 
        blank=True,
        help_text="Icône Bootstrap Icons (ex: bi-egg-fried)"
    )
    
    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titre")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Slug")
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE,
        related_name='courses',
        verbose_name="Catégorie"
    )
    description = models.TextField(verbose_name="Description courte")
    detailed_description = models.TextField(verbose_name="Description détaillée")
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name="Prix (FG)"
    )
    
    # Champ pour les images uploadées
    image = models.ImageField(
        upload_to='courses/',
        blank=True,
        null=True,
        verbose_name="Image uploadée"
    )
    
    # Champ pour les images statiques
    static_image_path = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Chemin image statique",
        help_text="Chemin relatif dans static/img/ (ex: 'courses/cuisine.jpg')"
    )
    
    instructor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='courses_taught',
        verbose_name="Formateur"
    )
    students = models.ManyToManyField(
        User,
        related_name='courses_enrolled',
        blank=True,
        verbose_name="Étudiants inscrits"
    )
    duration_weeks = models.PositiveSmallIntegerField(
        default=4,
        verbose_name="Durée (semaines)"
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name="Mise en avant"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de modification")

    class Meta:
        verbose_name = "Cours"
        verbose_name_plural = "Cours"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['created_at']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('course_detail', kwargs={'slug': self.slug})

    @property
    def image_url(self):
        """Retourne l'URL de l'image en priorisant le chemin statique"""
        if self.static_image_path:
            return f'/static/img/{self.static_image_path}'
        elif self.image:
            return self.image.url
        return '/static/img/default-course.jpg'

    def student_count(self):
        return self.students.count()

class CourseModule(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='modules',
        verbose_name="Cours"
    )
    title = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(verbose_name="Description")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre")
    duration_hours = models.PositiveSmallIntegerField(
        default=2,
        verbose_name="Durée (heures)"
    )

    class Meta:
        verbose_name = "Module"
        verbose_name_plural = "Modules"
        ordering = ['order']
        constraints = [
            models.UniqueConstraint(
                fields=['course', 'order'],
                name='unique_module_order'
            ),
        ]

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class Resource(models.Model):
    RESOURCE_TYPES = [
        ('INGREDIENTS', 'Ingrédients Clés'),
        ('CERTIFICATION', 'Certification'),
        ('COMMUNITY', 'Communauté'),
        ('TOOLS', 'Ressources'),
        ('RECIPE', 'Fiche recette'),
    ]
    
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='resources',
        verbose_name="Cours"
    )
    resource_type = models.CharField(
        max_length=20,
        choices=RESOURCE_TYPES,
        verbose_name="Type de ressource"
    )
    title = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(verbose_name="Description")
    static_image_path = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Chemin image statique"
    )
    file = models.FileField(
        upload_to='resources/files/',
        null=True,
        blank=True,
        verbose_name="Fichier joint"
    )
    external_url = models.URLField(
        blank=True,
        null=True,
        verbose_name="Lien externe"
    )

    class Meta:
        verbose_name = "Ressource"
        verbose_name_plural = "Ressources"
        ordering = ['resource_type', 'title']

    def __str__(self):
        return f"{self.get_resource_type_display()} - {self.title}"

    @property
    def image_url(self):
        if self.static_image_path:
            return f'/static/img/{self.static_image_path}'
        return '/static/img/default-resource.png'

    def get_icon(self):
        icons = {
            'INGREDIENTS': 'bi-basket',
            'CERTIFICATION': 'bi-award',
            'COMMUNITY': 'bi-people',
            'TOOLS': 'bi-tools',
            'RECIPE': 'bi-journal-text',
        }
        return icons.get(self.resource_type, 'bi-file-earmark')