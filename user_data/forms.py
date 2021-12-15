from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.files import images
from django.forms.models import ModelFormMetaclass
from .validators import validate_date_of_birth, validate_image
from django.contrib.auth.hashers import check_password

_MALES = (
    ('None', ''),
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),    
)

def password_check(p1, p2):    
    if not check_password(p1, p2):
        raise ValidationError("Incorrect password!")
    else:        
        return p1


class LoginForm(forms.Form):
    username_or_mail = forms.CharField(label='Login or e-mail', max_length=150)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean_username_or_mail(self):
        login = self.cleaned_data['username_or_mail']
        if User.objects.filter(email=login).exists():
            return User.objects.get(email=login)
        elif User.objects.filter(username=login).exists():
            return login
        else:    
            raise ValidationError('User does not exist!')

class RegisterForm(forms.Form):
    username = forms.CharField(label='Login', max_length=150)
    first_name = forms.CharField(label='First name', max_length=20)
    last_name = forms.CharField(label='Last name', max_length=40)
    male = forms.ChoiceField(label="Male", choices=_MALES, required=False)
    email = forms.EmailField(label='E-mail address', max_length=150)
    password = forms.CharField(label='Password', widget=forms.PasswordInput, validators=[validate_password])
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    def clean(self):
        cd = super().clean()
        username = cd.get('username')
        email = cd.get('email')
        pwd = cd.get('password')
        pwd2 = cd.get('password2')
        
        if "@" in username:
            raise ValidationError("'@' is forbidden in username!")

        if User.objects.filter(username=username).exists(): #username existance
            raise ValidationError('Username already exists!')

        if User.objects.filter(email=email).exists(): # email existence
            raise ValidationError("Email address already exists!")

        if pwd != pwd2: #password confirmation
            raise ValidationError('Passwords do not match!')
        
        return cd
        
class DateInput(forms.DateInput):
    input_type = 'date'

class AdditionalInfoForm(forms.Form):
    first_name = forms.CharField(label='First name', max_length=20)
    last_name = forms.CharField(label='Last name', max_length=40)
    male = forms.ChoiceField(label="Male", choices=_MALES, required=False)
    date_of_birth = forms.DateTimeField(label="Date of birth", required=False, widget=DateInput)
    about = forms.CharField(label='Tell us about yourself', widget=forms.Textarea(), required=False)
    image = forms.ImageField(label="Profile picture", required=False)

    def clean_image(self):
        avaible_formats = [
            'png',
            'jpeg',
            'jpg',
            ]
        img = self.files.get('image')
        if img:
            img_ext = img.name.split(".")[-1]
            if img.size > 4194304:
                raise ValidationError("Image size must be less than 4MB")
            if img_ext not in avaible_formats:
                raise ValidationError("Image extension is not avaible")        
        return img

    def clean_date_of_birth(self):
        date = self.cleaned_data['date_of_birth']
        if date:
            return validate_date_of_birth(date)

class ChangeUsername(forms.ModelForm): 
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ChangeUsername, self).__init__(*args, **kwargs)

    def clean_password(self):
        pwd = self.cleaned_data['password']
        return password_check(pwd, self.user.password)

class TypePassword(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields =['password']

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(TypePassword, self).__init__(*args, **kwargs)

    def clean_password(self):
        pwd = self.cleaned_data['password']
        print(pwd)
        return password_check(pwd, self.user.password)

class ChangeEmail(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['email', 'password']

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ChangeEmail, self).__init__(*args, **kwargs)
    
    def clean_password(self):
        pwd = self.cleaned_data['password']
        return password_check(pwd, self.user.password)

class PasswordResetForm(forms.Form):
    email = forms.EmailField(label='E-mail address', max_length=150, required=False)

class PasswordChange(forms.Form):
    old_password = forms.CharField(label='Old password', widget=forms.PasswordInput)
    new_password = forms.CharField(label='New password', widget=forms.PasswordInput, validators=[validate_password])
    new_password2 = forms.CharField(label='Confirm new password', widget=forms.PasswordInput)

    def clean_new_password(self):
        pwd = self.cleaned_data['new_password']
        pwd2 = self.cleaned_data['new_password2']
        if pwd != pwd2:
            raise ValidationError("Passwords do not match!")
        else:
            return pwd