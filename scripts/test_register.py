import os
import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE','grade_system.settings')
sys.path.insert(0, os.getcwd())
import django
django.setup()
from django.test import Client
c=Client()
resp = c.post('/courses/register/', {'username':'newstudent2', 'password1':'pass1234', 'password2':'pass1234'}, follow=True)
print('Register status', resp.status_code)
print(resp.content.decode('utf-8')[:5000])
print('Can login?', c.login(username='newstudent2', password='pass1234'))
