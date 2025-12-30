from django.apps import AppConfig

class CoursesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'courses'
    verbose_name = '課程管理'

class CoursesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'grade_system.courses'
    verbose_name = '課程管理'
    
    def ready(self):
        import grade_system.courses.signals