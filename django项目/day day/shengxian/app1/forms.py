from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core import validators
from .models import User


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields

    email = forms.EmailField()

class AddrForm(forms.Form):
    name = forms.CharField(validators=[
        validators.RegexValidator(regex=r'^\w{2,20}$',message='姓名为2-20位汉语，字母或下划线')
    ])
    addr = forms.CharField(validators=[
        validators.RegexValidator(regex=r'^\w{2,50}$',message='地址为2-50位')
    ])
    postcode = forms.CharField(validators=[
        validators.RegexValidator(regex=r'^\d{6}$',message='邮编为6位数字')
    ])
    tel = forms.CharField(validators=[
        validators.RegexValidator(regex=r'^\d{11}$',message='电话为11位数字')
    ])