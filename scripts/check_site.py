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
    # 先測試公開頁面
    for path in ['/', '/courses/', '/accounts/login/', '/courses/CS101/']:
        r = c.get(path, follow=True)
        print('\nGET', path, '->', r.status_code)
        print('TEMPLATES:', [t.name for t in getattr(r, 'templates', [])])
        print('LENGTH', len(r.content))
        print('BODY PREVIEW:\n', r.content.decode('utf-8')[:800])

    # 使用學生登入並測試學生頁面
    logged_in = c.login(username='student1', password='student123')
    print('\nLOGIN student1 ->', logged_in)
    for path in ['/courses/list/', '/courses/enroll/', '/courses/course/CS101/comment/add/']:
        r = c.get(path, follow=True)
        print('\nGET', path, '->', r.status_code)
        print('TEMPLATES:', [t.name for t in getattr(r, 'templates', [])])
        print('LENGTH', len(r.content))
        print('BODY PREVIEW:\n', r.content.decode('utf-8')[:800])

    # 使用教師登入並測試教師頁面
    c.logout()
    logged_in = c.login(username='teacher1', password='teacher123')
    print('\nLOGIN teacher1 ->', logged_in)
    for path in ['/courses/teacher/', '/courses/add/', '/courses/course/CS101/grade/']:
        r = c.get(path, follow=True)
        print('\nGET', path, '->', r.status_code)
        print('TEMPLATES:', [t.name for t in getattr(r, 'templates', [])])
        print('LENGTH', len(r.content))
        print('BODY PREVIEW:\n', r.content.decode('utf-8')[:800])

except TemplateDoesNotExist as e:
    print('TemplateDoesNotExist:', e)
except Exception as e:
    import traceback
    traceback.print_exc()