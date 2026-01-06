import os
import sys
import django
from django.template import TemplateDoesNotExist

print('CWD', os.getcwd())
print('SYSPATH[0:5]', sys.path[:5])
print('FILES', os.listdir('.'))
print('GRADE_DIR', os.path.isdir('grade_system'))
if os.path.isdir('grade_system'):
    print('GRADE_LIST', os.listdir('grade_system')[:20])

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grade_system.settings')
# ensure project root in sys.path
sys.path.insert(0, os.getcwd())
django.setup()

from django.test import Client

c = Client()
try:
    paths = ['/', '/courses/', '/accounts/login/']
    for path in paths:
        r = c.get(path, follow=True)
        print('\nGET', path, '->', r.status_code)
        print('TEMPLATES:', [t.name for t in getattr(r, 'templates', [])])
        print('LENGTH', len(r.content))
        print('BODY PREVIEW:\n', r.content.decode('utf-8')[:1000])

    # 先登入學生，再取用需要登入的頁面
    logged_in = c.login(username='student1', password='student123')
    print('\nLOGIN student1 ->', logged_in)
    r = c.get('/courses/list/', follow=True)
    print('GET /courses/list/ ->', r.status_code)
    print('TEMPLATES:', [t.name for t in getattr(r, 'templates', [])])
    print('LENGTH', len(r.content))
    print('BODY PREVIEW:\n', r.content.decode('utf-8')[:1000])

except TemplateDoesNotExist as e:
    print('TemplateDoesNotExist:', e)
except Exception as e:
    import traceback
    traceback.print_exc()