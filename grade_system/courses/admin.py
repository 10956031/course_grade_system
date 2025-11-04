from django.contrib import admin
from .models import Course, StudentCourse

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_id', 'course_name', 'teacher', 'credit']
    search_fields = ['course_id', 'course_name', 'teacher']

@admin.register(StudentCourse)
class StudentCourseAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'midterm_score', 'final_score', 'get_total_score']
    list_filter = ['course', 'student']
    search_fields = ['student__username', 'course__course_name']