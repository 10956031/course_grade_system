from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('list/', views.course_list, name='course_list'),
    path('course/<str:course_id>/', views.course_detail, name='course_detail'),
    path('course/<str:course_id>/grade/', views.grade_management, name='grade_management'),
    path('add/', views.add_course, name='add_course'),
    path('enroll/', views.manage_enrollment, name='manage_enrollment'),

]