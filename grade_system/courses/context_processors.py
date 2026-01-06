from .models import UserProfile


def user_role(request):
    """Provide user_role to all templates"""
    try:
        if request.user.is_authenticated:
            return {'user_role': getattr(request.user.profile, 'role', None)}
    except Exception:
        pass
    return {'user_role': None}
