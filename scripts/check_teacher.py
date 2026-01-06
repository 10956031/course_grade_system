import os
import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE','grade_system.settings')
sys.path.insert(0, os.getcwd())
import django
django.setup()
from django.test import Client
c=Client()
print('login teacher', c.login(username='teacher1', password='teacher123'))
r=c.get('/courses/course/CS101/grade/')
print('CS101 grade status', r.status_code)
print(r.content.decode('utf-8')[:1000])
