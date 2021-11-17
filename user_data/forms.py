from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class LoginForm(forms.Form):
    username_or_mail = forms.CharField(label='Login or e-mail', max_length=150)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean_username_or_mail(self):
        login = self.cleaned_data['username_or_mail']
        if User.objects.filter(email=login).exists():
            return User.objects.get(email=cd['username_or_mail'])
        elif User.objects.filter(username=login).exists():
            return login
        else:    
            raise ValidationError('User does not exist!')

class RegisterForm(forms.Form):
    username = forms.CharField(label='Login', max_length=150)
    first_name = forms.CharField(label='First name', max_length=20)
    last_name = forms.CharField(label='Last name', max_length=40)
    email = forms.EmailField(label='E-mail address', max_length=150)
    password = forms.CharField(label='Password', widget=forms.PasswordInput, validators=[validate_password])
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    def clean(self):
        cd = super().clean()
        username = cd.get('username')
        email = cd.get('email')
        pwd = cd.get('password')
        pwd2 = cd.get('password2')
        
        if User.objects.filter(username=username).exists():
            raise ValidationError('Username already exists!')

        if User.objects.filter(email=email).exists():
            raise ValidationError("Email address already exists!")

        if pwd != pwd2: #password confirmation
            raise ValidationError('Passwords do not match!')
        
        return cd
        

class AdditionalInfoForm(forms.Form):
    first_name = forms.CharField(label='First name', max_length=20)
    last_name = forms.CharField(label='Last name', max_length=40)
    date_of_birth = forms.DateField(label="Date of birth", required=False)
    about = forms.CharField(label='Tell us about yourself', widget=forms.Textarea(), required=False)
    profile_pic = forms.ImageField(required=False)

class ChangeUsernameOrMailForm(forms.Form):
    username = forms.CharField(label='Your new login', max_length=150, required=False)
    email = forms.EmailField(label='E-mail address', max_length=150, required=False)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class PasswordResetForm(forms.Form):
    email = forms.EmailField(label='E-mail address', max_length=150, required=False)

class PasswordChange(forms.Form):
    old_password = forms.CharField(label='Old password', widget=forms.PasswordInput)
    new_password = forms.CharField(label='New password', widget=forms.PasswordInput, validators=[validate_password])
    new_password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    def clean_new_password(self):
        pwd = self.cleaned_data['new_password']
        pwd2 = self.cleaned_data['new_password2']
        if pwd != pwd2:
            raise ValidationError("Passwords do not match!")
        else:
            return pwd