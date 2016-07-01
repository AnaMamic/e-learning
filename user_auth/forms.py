from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import CustomUser


class RegistrationForm(forms.ModelForm):
        username        = forms.CharField(label='Username')
        email           = forms.EmailField(label='Email Address')
        password        = forms.CharField(label='Password', widget=forms.PasswordInput(render_value=False))
        password1       = forms.CharField(label='Verify Password', widget=forms.PasswordInput(render_value=False))
        professor       = forms.BooleanField(label='Professor', initial=False, required=False)

        

        class Meta:
                model = CustomUser
                fields = [
                        "professor",
                        "first_name", 
                        "last_name",
                ]
                exclude = ('user',)


        def clean_username(self):
                username = self.cleaned_data.get('username')
                try:
                        User.objects.get(username=username)
                except User.DoesNotExist:
                        return username
                raise forms.ValidationError('That username is already taken, please select another.')

        def clean_email(self): 
                email = self.cleaned_data.get('email')
                email_qs = User.objects.filter(email=email)
                if email_qs.exists(): 
                        raise forms.ValidationError('Email Already Registered')
                return email

        def clean(self):
                ### password mora bit upisan 
                if 'password' in self.cleaned_data and self.cleaned_data.get('password') != self.cleaned_data.get('password1'):
                        raise forms.ValidationError('The passwords did not match.  Please try again.')
                return self.cleaned_data

class LoginForm(forms.Form):
        username        = forms.CharField(label='User Name')
        password        = forms.CharField(label='Password', widget=forms.PasswordInput(render_value=False))
