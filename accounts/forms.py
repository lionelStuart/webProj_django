from django import forms
from django.contrib.auth.models import User


class UserRegistrationForm(forms.ModelForm):
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

