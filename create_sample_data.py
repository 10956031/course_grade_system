import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grade_system.settings')
django.setup()

from django.contrib.auth.models import User
from grade_system.courses.models import Course, StudentCourse

def create_sample_data():
    # 建立測試學生
    student, created = User.objects.get_or_create(
        username='teststudent',
        defaults={'email': 'student@example.com'}
    )
    if created:
        student.set_password('testpassword123')
        student.save()
    
    # 建立三門課程
    courses_data = [
        {'course_id': 'CS101', 'course_name': '程式設計導論', 'teacher': '張老師', 'credit': 3},
        {'course_id': 'MA201', 'course_name': '微積分', 'teacher': '李老師', 'credit': 4},
        {'course_id': 'PH301', 'course_name': '物理學', 'teacher': '王老師', 'credit': 3},
    ]
    
    for course_data in courses_data:
        course, created = Course.objects.get_or_create(
            course_id=course_data['course_id'],
            defaults=course_data
        )
        
        # 讓學生修這些課
        StudentCourse.objects.get_or_create(
            student=student,
            course=course,
            defaults={
                'midterm_score': 85.0,
                'final_score': 90.0
            }
        )
    
    print("範例資料建立完成！")

if __name__ == '__main__':
    create_sample_data()