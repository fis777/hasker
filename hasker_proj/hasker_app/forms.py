""" forms """
from django import forms
from .models import Profile, Question, Answer
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'email', 'password')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('user', 'avatar')

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('title', 'question')

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer']

class AddUserForm(forms.Form):
    nickname = forms.CharField(label="nickname", max_length=20, min_length=3)
    email = forms.EmailField(widget=forms.EmailInput)
    password = forms.CharField(label="password", max_length=32, min_length=6, widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="confirm", max_length=32, min_length=6, widget=forms.PasswordInput)

class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = {'username', 'email'} 

class ImageUploadForm(forms.Form):
    image = forms.ImageField()

class LoginUser(forms.Form):
    username = forms.CharField(label="Username", max_length=20, min_length=3)
    password = forms.CharField(label="Password", max_length=32, min_length=6, widget=forms.PasswordInput)
