import os
import django
import sys

# 添加專案目錄到 Python 路徑
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grade_system.settings')
django.setup()

from django.contrib.auth.models import User
from courses.models import Course, StudentCourse, CourseComment, UserProfile

def create_sample_data():
    print("開始建立範例資料...")
    
    # 建立管理者
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@example.com',
            'first_name': '系統',
            'last_name': '管理員',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        admin_user.profile.role = 'admin'
        admin_user.profile.save()
        print(f"建立管理者: {admin_user.username}")
    
    # 建立教師
    teacher_user, created = User.objects.get_or_create(
        username='teacher1',
        defaults={
            'email': 'teacher1@example.com',
            'first_name': '張',
            'last_name': '老師'
        }
    )
    if created:
        teacher_user.set_password('teacher123')
        teacher_user.save()
        teacher_user.profile.role = 'teacher'
        teacher_user.profile.department = '資訊工程學系'
        teacher_user.profile.save()
        print(f"建立教師: {teacher_user.username}")
    
    # 建立學生
    students = [
        {
            'username': 'student1',
            'email': 'student1@example.com',
            'first_name': '王',
            'last_name': '小明',
            'student_id': 'S1105001',
            'department': '資訊工程學系'
        },
        {
            'username': 'student2',
            'email': 'student2@example.com',
            'first_name': '林',
            'last_name': '小華',
            'student_id': 'S1105002',
            'department': '資訊工程學系'
        },
    ]
    
    student_users = []
    for student_data in students:
        user, created = User.objects.get_or_create(
            username=student_data['username'],
            defaults={
                'email': student_data['email'],
                'first_name': student_data['first_name'],
                'last_name': student_data['last_name']
            }
        )
        if created:
            user.set_password('student123')
            user.save()
            user.profile.role = 'student'
            user.profile.student_id = student_data['student_id']
            user.profile.department = student_data['department']
            user.profile.save()
            student_users.append(user)
            print(f"建立學生: {user.username}")
    
    # 建立課程
    courses_data = [
        {
            'course_id': 'CS101',
            'course_name': '程式設計導論',
            'teacher': teacher_user,
            'credit': 3,
            'description': '學習程式設計基礎概念與實作'
        },
        {
            'course_id': 'CS201',
            'course_name': '資料結構',
            'teacher': teacher_user,
            'credit': 3,
            'description': '學習各種資料結構與演算法'
        },
        {
            'course_id': 'MA101',
            'course_name': '微積分',
            'teacher': teacher_user,
            'credit': 4,
            'description': '學習微分與積分的基本概念'
        },
    ]
    
    courses = []
    for course_data in courses_data:
        course, created = Course.objects.get_or_create(
            course_id=course_data['course_id'],
            defaults=course_data
        )
        if created:
            courses.append(course)
            print(f"建立課程: {course.course_name}")
    
    # 讓學生修課
    for student in student_users:
        for i, course in enumerate(courses):
            student_course, created = StudentCourse.objects.get_or_create(
                student=student,
                course=course,
                defaults={
                    'midterm_score': 80 + i * 5,
                    'final_score': 85 + i * 5
                }
            )
            if created:
                print(f"學生 {student.username} 已修習 {course.course_name}")
    
    # 建立留言
    comments_data = [
        {
            'course': courses[0],
            'student': student_users[0],
            'content': '這門課很有趣，老師講解得很清楚！'
        },
        {
            'course': courses[0],
            'student': student_users[1],
            'content': '作業有點難，但學到很多實用的知識。'
        },
        {
            'course': courses[1],
            'student': student_users[0],
            'content': '資料結構很有挑戰性，但學好後對程式設計幫助很大。'
        },
    ]
    
    for comment_data in comments_data:
        comment, created = CourseComment.objects.get_or_create(
            course=comment_data['course'],
            student=comment_data['student'],
            defaults={'content': comment_data['content']}
        )
        if created:
            print(f"建立留言: {comment.student.username} 在 {comment.course.course_name}")
    
    print("\n範例資料建立完成！")
    print("\n測試帳號資訊：")
    print("1. 管理者")
    print("   帳號: admin")
    print("   密碼: admin123")
    print("   角色: 管理員 (可建立教師帳號)")
    
    print("\n2. 教師")
    print("   帳號: teacher1")
    print("   密碼: teacher123")
    print("   角色: 教師 (可建立課程、管理成績)")
    
    print("\n3. 學生")
    print("   帳號: student1")
    print("   密碼: student123")
    print("   學號: S1105001")
    print("\n   帳號: student2")
    print("   密碼: student123")
    print("   學號: S1105002")

if __name__ == '__main__':
    create_sample_data()