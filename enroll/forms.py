from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import NewQueryInfo, Address

class SignUpForm(UserCreationForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        labels = {
            'username': "Username",
            'email': "Email Address"
        }


class QueryForm(forms.ModelForm):
    class Meta:
        model = NewQueryInfo
        fields = '__all__'

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['locality', 'city', 'state', 'zipcode']
        widgets = {'zipcode': forms.NumberInput(attrs={'placeholder':'Enter your zipcode'})}