from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Avg, Count, Sum
from django.db import transaction
from django.core.paginator import Paginator
from .models import Course, StudentCourse, CourseComment, UserProfile
from .forms import (
    CustomUserCreationForm, UserProfileForm, UserUpdateForm,
    CourseForm, EnrollmentForm, GradeForm, CourseCommentForm
)
from .decorators import teacher_required, student_required, admin_required

def home(request):
    """首頁"""
    return render(request, 'home.html')

def register(request):
    """學生註冊"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # 設定為學生角色
            user.profile.role = 'student'
            user.profile.save()
            
            # 自動登入
            login(request, user)
            messages.success(request, '註冊成功！歡迎使用成績系統')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    """個人資料管理"""
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, '個人資料已更新！')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.profile)
    
    # 取得學生修課統計
    if request.user.profile.role == 'student':
        student_courses = StudentCourse.objects.filter(student=request.user)
        total_courses = student_courses.count()
        avg_score = student_courses.aggregate(
            avg=Avg('final_score')
        )['avg']
    else:
        total_courses = avg_score = 0
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'total_courses': total_courses,
        'avg_score': avg_score,
    }
    return render(request, 'registration/profile.html', context)

@student_required
def course_list(request):
    """學生課程列表"""
    student_courses = StudentCourse.objects.filter(student=request.user).select_related('course')
    
    # 計算統計資料
    courses_with_avg = []
    total_score = 0
    total_credits = 0
    count = 0
    
    for sc in student_courses:
        avg_score = sc.get_total_score()
        grade = sc.get_grade()
        
        if avg_score is not None:
            total_score += avg_score * sc.course.credit
            total_credits += sc.course.credit
            count += 1
        
        courses_with_avg.append({
            'course': sc.course,
            'midterm_score': sc.midterm_score,
            'final_score': sc.final_score,
            'average_score': avg_score,
            'grade': grade,
        })
    
    # 計算加權平均
    weighted_avg = total_score / total_credits if total_credits > 0 else 0
    
    context = {
        'courses': courses_with_avg,
        'weighted_avg': round(weighted_avg, 2),
        'total_credits': total_credits,
        'student': request.user
    }
    return render(request, 'courses/course_list.html', context)

@login_required
def course_detail(request, course_id):
    """課程詳細資訊"""
    course = get_object_or_404(Course, course_id=course_id)
    
    # 取得留言
    comments = CourseComment.objects.filter(course=course).select_related('student').order_by('-created_at')
    
    # 分頁
    paginator = Paginator(comments, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'course': course,
        'page_obj': page_obj,
    }
    
    # 如果是學生，顯示成績資訊
    if request.user.profile.role == 'student':
        try:
            student_course = StudentCourse.objects.get(course=course, student=request.user)
            context['student_course'] = student_course
        except StudentCourse.DoesNotExist:
            pass
    
    return render(request, 'courses/course_detail.html', context)

@teacher_required
def teacher_courses(request):
    """教師授課列表"""
    courses = Course.objects.filter(teacher=request.user).annotate(
        student_count=Count('enrollments')
    )
    
    context = {
        'courses': courses,
    }
    return render(request, 'courses/teacher_courses.html', context)

@teacher_required
def grade_management(request, course_id):
    """教師成績管理"""
    course = get_object_or_404(Course, course_id=course_id, teacher=request.user)
    
    if request.method == 'POST':
        # 處理批量成績更新
        for key, value in request.POST.items():
            if key.startswith('midterm_'):
                student_id = key.split('_')[1]
                try:
                    enrollment = StudentCourse.objects.get(
                        course=course, 
                        student_id=student_id
                    )
                    if value:
                        enrollment.midterm_score = value
                        enrollment.save()
                except (StudentCourse.DoesNotExist, ValueError):
                    pass
            elif key.startswith('final_'):
                student_id = key.split('_')[1]
                try:
                    enrollment = StudentCourse.objects.get(
                        course=course, 
                        student_id=student_id
                    )
                    if value:
                        enrollment.final_score = value
                        enrollment.save()
                except (StudentCourse.DoesNotExist, ValueError):
                    pass
        
        messages.success(request, '成績已更新！')
        return redirect('grade_management', course_id=course_id)
    
    # 取得修課學生
    enrollments = StudentCourse.objects.filter(course=course).select_related('student')
    
    context = {
        'course': course,
        'enrollments': enrollments,
    }
    return render(request, 'courses/grade_management.html', context)

@teacher_required
def add_course(request):
    """教師新增課程"""
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            # 預設為當前教師
            if not course.teacher:
                course.teacher = request.user
            course.save()
            messages.success(request, '課程新增成功！')
            return redirect('teacher_courses')
    else:
        form = CourseForm(initial={'teacher': request.user})
    
    return render(request, 'courses/add_course.html', {'form': form})

@student_required
def manage_enrollment(request):
    """學生加選/退選課程"""
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            course = form.cleaned_data['course']
            action = form.cleaned_data['action']
            
            if action == 'enroll':
                # 檢查是否已修過
                if not StudentCourse.objects.filter(student=request.user, course=course).exists():
                    StudentCourse.objects.create(student=request.user, course=course)
                    messages.success(request, f'成功加選課程: {course.course_name}')
                else:
                    messages.warning(request, f'您已經修習此課程: {course.course_name}')
            elif action == 'drop':
                # 退選課程
                deleted_count, _ = StudentCourse.objects.filter(student=request.user, course=course).delete()
                if deleted_count > 0:
                    messages.success(request, f'成功退選課程: {course.course_name}')
                else:
                    messages.warning(request, f'您未修習此課程: {course.course_name}')
            
            return redirect('course_list')
    else:
        form = EnrollmentForm()
    
    # 取得可選課程（未修習的）
    enrolled_courses = StudentCourse.objects.filter(student=request.user).values_list('course_id', flat=True)
    available_courses = Course.objects.exclude(id__in=enrolled_courses)
    
    context = {
        'form': form,
        'available_courses': available_courses,
        'enrolled_courses': StudentCourse.objects.filter(student=request.user).select_related('course')
    }
    return render(request, 'courses/manage_enrollment.html', context)

@student_required
def add_comment(request, course_id):
    """學生新增留言"""
    course = get_object_or_404(Course, course_id=course_id)
    
    # 檢查是否修過此課
    if not StudentCourse.objects.filter(student=request.user, course=course).exists():
        messages.error(request, '您未修習此課程，無法留言')
        return redirect('course_detail', course_id=course_id)
    
    if request.method == 'POST':
        form = CourseCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.course = course
            comment.student = request.user
            comment.save()
            messages.success(request, '留言已發表！')
            return redirect('course_detail', course_id=course_id)
    else:
        form = CourseCommentForm()
    
    context = {
        'form': form,
        'course': course,
    }
    return render(request, 'comments/add_comment.html', context)

@student_required
def edit_comment(request, comment_id):
    """學生編輯留言"""
    comment = get_object_or_404(CourseComment, id=comment_id, student=request.user)
    
    if request.method == 'POST':
        form = CourseCommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.is_edited = True
            comment.save()
            messages.success(request, '留言已更新！')
            return redirect('course_detail', course_id=comment.course.course_id)
    else:
        form = CourseCommentForm(instance=comment)
    
    context = {
        'form': form,
        'comment': comment,
    }
    return render(request, 'comments/edit_comment.html', context)

@student_required
def delete_comment(request, comment_id):
    """學生刪除留言"""
    comment = get_object_or_404(CourseComment, id=comment_id, student=request.user)
    course_id = comment.course.course_id
    
    if request.method == 'POST':
        comment.delete()
        messages.success(request, '留言已刪除！')
    
    return redirect('course_detail', course_id=course_id)