from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('list/', views.course_list, name='course_list'),
    path('teacher/', views.teacher_courses, name='teacher_courses'),
    path('course/<str:course_id>/', views.course_detail, name='course_detail'),
    path('course/<str:course_id>/grade/', views.grade_management, name='grade_management'),
    path('course/<str:course_id>/comment/add/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('add/', views.add_course, name='add_course'),
    path('enroll/', views.manage_enrollment, name='manage_enrollment'),

]