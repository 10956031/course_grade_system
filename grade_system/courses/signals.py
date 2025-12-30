from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """當使用者建立時，自動建立使用者資料"""
    if created:
        UserProfile.objects.create(user=instance)
        # 預設為學生角色
        instance.profile.role = 'student'
        instance.profile.save()

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """儲存使用者時，同時儲存使用者資料"""
    try:
        instance.profile.save()
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)