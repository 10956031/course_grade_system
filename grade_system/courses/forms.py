from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Course, StudentCourse, CourseComment, UserProfile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='電子郵件')
    first_name = forms.CharField(max_length=30, required=True, label='名字')
    last_name = forms.CharField(max_length=30, required=True, label='姓氏')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        labels = {
            'username': '使用者名稱',
        }
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar', 'student_id', 'department']
        labels = {
            'avatar': '頭像',
            'student_id': '學號',
            'department': '系所',
        }

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': '名字',
            'last_name': '姓氏',
            'email': '電子郵件',
        }

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_id', 'course_name', 'teacher', 'credit', 'description']
        labels = {
            'course_id': '課號',
            'course_name': '課名',
            'teacher': '任課老師',
            'credit': '學分數',
            'description': '課程描述',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 只顯示教師
        self.fields['teacher'].queryset = User.objects.filter(profile__role='teacher')

class EnrollmentForm(forms.Form):
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        label='選擇課程',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    action = forms.ChoiceField(
        choices=[('enroll', '加選'), ('drop', '退選')],
        label='操作',
        widget=forms.RadioSelect
    )

class GradeForm(forms.ModelForm):
    class Meta:
        model = StudentCourse
        fields = ['midterm_score', 'final_score']
        labels = {
            'midterm_score': '期中考分數',
            'final_score': '期末考分數',
        }
        widgets = {
            'midterm_score': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'max': '100'}),
            'final_score': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'max': '100'}),
        }

class CourseCommentForm(forms.ModelForm):
    class Meta:
        model = CourseComment
        fields = ['content']
        labels = {
            'content': '留言內容',
        }
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': '請輸入留言...'}),
        }