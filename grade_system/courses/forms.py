from django import forms
from .models import Course, StudentCourse

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_id', 'course_name', 'teacher', 'credit']
        labels = {
            'course_id': '課號',
            'course_name': '課名',
            'teacher': '任課老師',
            'credit': '學分數',
        }

class EnrollmentForm(forms.Form):
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        label='選擇課程'
    )
    action = forms.ChoiceField(
        choices=[('enroll', '加選'), ('drop', '退選')],
        label='操作',
        widget=forms.RadioSelect
    )