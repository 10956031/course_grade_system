from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Avg
from .models import Course, StudentCourse
from .forms import CourseForm, EnrollmentForm

def home(request):
    return render(request, 'home.html')

@login_required
def course_list(request):
    # 取得當前學生修的所有課程
    student_courses = StudentCourse.objects.filter(student=request.user).select_related('course')
    
    # 計算平均分數
    courses_with_avg = []
    total_avg = 0
    count = 0
    
    for sc in student_courses:
        avg_score = sc.get_total_score()
        if avg_score:
            total_avg += avg_score
            count += 1
        
        courses_with_avg.append({
            'course': sc.course,
            'midterm_score': sc.midterm_score,
            'final_score': sc.final_score,
            'average_score': avg_score
        })
    
    overall_avg = total_avg / count if count > 0 else 0
    
    context = {
        'courses': courses_with_avg,
        'overall_avg': round(overall_avg, 2),
        'student': request.user
    }
    return render(request, 'course_list.html', context)

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, course_id=course_id)
    student_course = get_object_or_404(StudentCourse, course=course, student=request.user)
    
    # 取得修這門課的所有學生
    enrolled_students = StudentCourse.objects.filter(course=course).select_related('student')
    
    context = {
        'course': course,
        'student_course': student_course,
        'enrolled_students': enrolled_students,
    }
    return render(request, 'course_detail.html', context)

@login_required
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm()
    
    return render(request, 'add_course.html', {'form': form})

@login_required
def manage_enrollment(request):
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            course = form.cleaned_data['course']
            action = form.cleaned_data['action']
            
            if action == 'enroll':
                # 加選課程
                if not StudentCourse.objects.filter(student=request.user, course=course).exists():
                    StudentCourse.objects.create(student=request.user, course=course)
            elif action == 'drop':
                # 退選課程
                StudentCourse.objects.filter(student=request.user, course=course).delete()
            
            return redirect('course_list')
    else:
        form = EnrollmentForm()
    
    return render(request, 'manage_enrollment.html', {'form': form})