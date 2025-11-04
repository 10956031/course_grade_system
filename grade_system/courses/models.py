from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    course_id = models.CharField(max_length=20, verbose_name='課號', unique=True)
    course_name = models.CharField(max_length=100, verbose_name='課名')
    teacher = models.CharField(max_length=50, verbose_name='任課老師')
    credit = models.PositiveIntegerField(verbose_name='學分數', default=3)
    
    class Meta:
        verbose_name = '課程'
        verbose_name_plural = '課程'
    
    def __str__(self):
        return f"{self.course_name} ({self.course_id})"

class StudentCourse(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='學生')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='課程')
    midterm_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='期中考分數')
    final_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='期末考分數')
    
    class Meta:
        verbose_name = '學生修課'
        verbose_name_plural = '學生修課'
        unique_together = ['student', 'course']
    
    def get_total_score(self):
        if self.midterm_score and self.final_score:
            return (self.midterm_score + self.final_score) / 2
        return None
    
    def __str__(self):
        return f"{self.student.username} - {self.course.course_name}"