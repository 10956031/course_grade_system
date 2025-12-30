from django.db import models
from django.contrib.auth.models import User, Group
from django.core.validators import MinValueValidator, MaxValueValidator

class UserProfile(models.Model):
    USER_ROLES = (
        ('student', '學生'),
        ('teacher', '教師'),
        ('admin', '管理者'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=USER_ROLES, default='student', verbose_name='角色')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='頭像')
    student_id = models.CharField(max_length=20, null=True, blank=True, verbose_name='學號')
    department = models.CharField(max_length=100, null=True, blank=True, verbose_name='系所')
    
    class Meta:
        verbose_name = '使用者資料'
        verbose_name_plural = '使用者資料'
    
    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

class Course(models.Model):
    course_id = models.CharField(max_length=20, verbose_name='課號', unique=True)
    course_name = models.CharField(max_length=100, verbose_name='課名')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, 
                               limit_choices_to={'profile__role': 'teacher'},
                               related_name='teaching_courses',
                               verbose_name='任課老師')
    credit = models.PositiveIntegerField(verbose_name='學分數', default=3)
    description = models.TextField(blank=True, verbose_name='課程描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='建立時間')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新時間')
    
    class Meta:
        verbose_name = '課程'
        verbose_name_plural = '課程'
        ordering = ['course_id']
    
    def __str__(self):
        return f"{self.course_name} ({self.course_id})"
    
    def get_student_count(self):
        return self.studentcourse_set.count()

class StudentCourse(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, 
                               limit_choices_to={'profile__role': 'student'},
                               related_name='enrolled_courses',
                               verbose_name='學生')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, 
                              related_name='enrollments',
                              verbose_name='課程')
    midterm_score = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True, 
        verbose_name='期中考分數',
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    final_score = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True, 
        verbose_name='期末考分數',
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    enrolled_at = models.DateTimeField(auto_now_add=True, verbose_name='選課時間')
    
    class Meta:
        verbose_name = '學生修課'
        verbose_name_plural = '學生修課'
        unique_together = ['student', 'course']
        ordering = ['-enrolled_at']
    
    def get_total_score(self):
        """計算平均分數"""
        if self.midterm_score is not None and self.final_score is not None:
            return (self.midterm_score + self.final_score) / 2
        return None
    
    def get_grade(self):
        """計算等第"""
        total = self.get_total_score()
        if total is None:
            return None
        if total >= 90:
            return 'A+'
        elif total >= 85:
            return 'A'
        elif total >= 80:
            return 'A-'
        elif total >= 77:
            return 'B+'
        elif total >= 73:
            return 'B'
        elif total >= 70:
            return 'B-'
        elif total >= 67:
            return 'C+'
        elif total >= 63:
            return 'C'
        elif total >= 60:
            return 'C-'
        else:
            return 'F'
    
    def __str__(self):
        return f"{self.student.username} - {self.course.course_name}"

class CourseComment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, 
                              related_name='comments',
                              verbose_name='課程')
    student = models.ForeignKey(User, on_delete=models.CASCADE, 
                               limit_choices_to={'profile__role': 'student'},
                               related_name='course_comments',
                               verbose_name='學生')
    content = models.TextField(verbose_name='留言內容')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='建立時間')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新時間')
    is_edited = models.BooleanField(default=False, verbose_name='已編輯')
    
    class Meta:
        verbose_name = '課程留言'
        verbose_name_plural = '課程留言'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.student.username} - {self.course.course_name}"