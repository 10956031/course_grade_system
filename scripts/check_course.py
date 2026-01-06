import os
import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE','grade_system.settings')
sys.path.insert(0, os.getcwd())
import django
django.setup()
from grade_system.courses.models import Course
try:
    c = Course.objects.get(course_id='CS101')
    print('Found CS101 teacher:', c.teacher.username)
    print('Course id:', c.course_id)
except Exception as e:
    print('Error', e)
