from django.http import HttpResponseForbidden
from functools import wraps

def teacher_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("請先登入")
        if not hasattr(request.user, 'profile') or request.user.profile.role != 'teacher':
            return HttpResponseForbidden("您不是教師，無法訪問此頁面")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def student_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("請先登入")
        if not hasattr(request.user, 'profile') or request.user.profile.role != 'student':
            return HttpResponseForbidden("您不是學生，無法訪問此頁面")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("請先登入")
        if not hasattr(request.user, 'profile') or request.user.profile.role != 'admin':
            return HttpResponseForbidden("您不是管理者，無法訪問此頁面")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# courses/context_processors.py
def user_role(request):
    """將使用者角色加入到模板上下文中"""
    if request.user.is_authenticated:
        try:
            return {'user_role': request.user.profile.role}
        except:
            return {'user_role': None}
    return {'user_role': None}