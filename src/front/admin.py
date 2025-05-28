from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Course, CourseModule, Resource

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 20

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'instructor',
        'price_display',
        'duration_display',
        'student_count',
        'is_featured',
        'image_preview'
    )
    list_filter = ('category', 'is_featured', 'created_at')
    search_fields = ('title', 'description')
    filter_horizontal = ('students',)
    readonly_fields = ('created_at', 'updated_at', 'student_count', 'image_preview')
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'category', 'instructor')
        }),
        ('Contenu', {
            'fields': ('description', 'detailed_description')
        }),
        ('Médias', {
            'fields': ('image', 'image_preview', 'static_image_path')
        }),
        ('Paramètres', {
            'fields': ('price', 'duration_weeks', 'is_featured', 'students')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def price_display(self, obj):
        return f"{obj.price} FG"
    price_display.short_description = "Prix"
    
    def duration_display(self, obj):
        return f"{obj.duration_weeks} semaine{'s' if obj.duration_weeks > 1 else ''}"
    duration_display.short_description = "Durée"
    
    def image_preview(self, obj):
        if obj.image_url:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.image_url)
        return "Aucune image"
    image_preview.short_description = "Aperçu"

@admin.register(CourseModule)
class CourseModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'duration_hours')
    list_filter = ('course',)
    search_fields = ('title', 'description')
    ordering = ('course', 'order')
    list_per_page = 20

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'resource_type_display', 'icon_preview')
    list_filter = ('course', 'resource_type')
    search_fields = ('title', 'description')
    readonly_fields = ('icon_preview',)
    fieldsets = (
        (None, {
            'fields': ('course', 'resource_type', 'title', 'description')
        }),
        ('Contenu', {
            'fields': ('static_image_path', 'file', 'external_url')
        }),
        ('Aperçu', {
            'fields': ('icon_preview',),
            'classes': ('collapse',)
        }),
    )
    
    def resource_type_display(self, obj):
        return obj.get_resource_type_display()
    resource_type_display.short_description = "Type"
    
    def icon_preview(self, obj):
        icon_class = obj.get_icon()
        return format_html('<i class="bi {}" style="font-size: 1.5rem;"></i> {}', icon_class, obj.get_resource_type_display())
    icon_preview.short_description = "Icône"