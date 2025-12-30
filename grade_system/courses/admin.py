from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Course, StudentCourse, CourseComment

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = '使用者資料'

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_role', 'is_staff')
    list_filter = ('profile__role', 'is_staff', 'is_superuser', 'is_active')
    
    def get_role(self, obj):
        return obj.profile.get_role_display()
    get_role.short_description = '角色'

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_id', 'course_name', 'teacher', 'credit', 'get_student_count', 'created_at']
    list_filter = ['teacher', 'credit']
    search_fields = ['course_id', 'course_name', 'teacher__username']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_student_count(self, obj):
        return obj.get_student_count()
    get_student_count.short_description = '修課人數'

@admin.register(StudentCourse)
class StudentCourseAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'midterm_score', 'final_score', 'get_total_score', 'get_grade', 'enrolled_at']
    list_filter = ['course', 'student']
    search_fields = ['student__username', 'course__course_name']
    readonly_fields = ['enrolled_at']
    
    def get_total_score(self, obj):
        return obj.get_total_score()
    get_total_score.short_description = '平均分數'
    
    def get_grade(self, obj):
        return obj.get_grade()
    get_grade.short_description = '等第'

@admin.register(CourseComment)
class CourseCommentAdmin(admin.ModelAdmin):
    list_display = ['course', 'student', 'created_at', 'updated_at', 'is_edited']
    list_filter = ['course', 'student', 'created_at']
    search_fields = ['content', 'student__username', 'course__course_name']
    readonly_fields = ['created_at', 'updated_at']

# 重新註冊 UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)