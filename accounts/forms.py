from django import forms
from django.contrib.auth.models import User

from .models import UserProfile


class UserRegistrationForm(forms.ModelForm):
    '''
    User Registration
    '''
    password = forms.CharField(label='password',
                               widget=forms.PasswordInput)
    password_check = forms.CharField(label='password',
                                     widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password_check(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password_check']:
            raise forms.ValidationError('Passwords don\'t match')
        return cd['password_check']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['birthday', 'photo']
