from django import forms
from django.forms import Textarea, TextInput, FileInput

from app.models import *


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(forms.Form, forms.ModelForm):
    login = forms.CharField(widget=TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'login'
            }),
        label='Login')
    email = forms.EmailField(widget=TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
        label='Email')
    first_name = forms.CharField(widget=TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'first_name'
            }),
        label='First_name')
    last_name = forms.CharField(widget=TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'last_name'
        }),
        label='Last_name')
    nickname = forms.CharField(widget=TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'nickname'
                }),
        label='Nickname')
    password = forms.CharField(widget=forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'password'
                }),
        label='Password')
    repeat_password = forms.CharField(widget=forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'repeat password'
                }),
        label='Repeat_password')

    class Meta:
        model = User
        fields = ['login', 'email', 'first_name', 'last_name', 'nickname', 'password', 'repeat_password']

    def clean_email(self):
        email = self.cleaned_data['email']
        check = User.objects.filter(email=email).exists()
        if check:
            self.add_error(None, 'Email already exists')
        else:
            return email

    def clean_login(self):
        login = self.cleaned_data['login']
        check = User.objects.filter(username=login).exists()
        if check:
            self.add_error(None, 'Login already exists')
        else:
            return login

    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']
        check = Profile.objects.filter(nickname=nickname).exists()
        if check:
            self.add_error(None, 'Nickname already exists')
        else:
            return nickname

    def clean(self):
        password = self.cleaned_data['password']
        repeat_password = self.cleaned_data['repeat_password']
        if password != repeat_password:
            self.add_error(None, 'Passwords does not math')
        return self.cleaned_data


class SettingsForm(forms.Form,forms.ModelForm):#forms.Form, forms.ModelForm):
    username = forms.CharField(required=False, disabled=True, widget=TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'username'
            }),
        label='Username')
    email = forms.EmailField(required=False, widget=TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
        label='Email')
    nickname = forms.CharField(required=False, widget=TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'nickname'
            }),
        label='Nickname')
    first_name = forms.CharField(required=False, widget=TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'first_name'
            }),
        label='First_name')
    last_name = forms.CharField(required=False, widget=TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'last_name'
            }),
        label='Last_name')
    avatar = forms.ImageField(required=False, widget=FileInput(attrs={
                'class': 'form-control'
            }),
        label='Avatar')

    def clean_email(self):
        email = self.cleaned_data['email']
        check = User.objects.filter(email=email).exists()
        if email == '':
            return email
        elif check:
            self.add_error(None, 'Email already exists')
        else:
            return email

    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']
        check = Profile.objects.filter(nickname=nickname).exists()
        if nickname == '':
            return nickname
        elif check:
            self.add_error(None, 'Nickname already exists')
        else:
            return nickname

    class Meta:
        model = User
        fields = ['username', 'email', 'nickname', 'first_name', 'last_name', 'avatar']

    def save(self, *args, **kwarg):
        user = super().save(*args, **kwarg)
        if self.cleaned_data['avatar']:
            user.profile.avatar = self.cleaned_data['avatar']
        user.profile.save()
        return user


class QuestionForm(forms.ModelForm):
    title = forms.CharField(widget=TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Title'
            }),
        label='Title')
    text = forms.Textarea()
    tag = forms.CharField(label='Tags', required=False, widget=TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tags'
            }))

    class Meta:
        model = Question
        fields = ['title', 'text', 'tag']

        widgets = {
            "text": Textarea(attrs={
                "class": "form-control",
                'placeholder': 'Very big text'
            })
        }
        labels = {
            'text': 'Text'
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['body']

        widgets = {
            "body": Textarea(attrs={
                "class": "form-control input-text",
                "rows": "5"
            })
        }