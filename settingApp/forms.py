
from django import forms
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.core.exceptions import ValidationError


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=250, required=True, label='',
      widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}))
    email = forms.EmailField(max_length=250, required=True, label='',
      widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}))

    class Meta:
        model = User
        fields =('username','email')
        

class UpdateUserPasswordForm(forms.ModelForm):
    password1 = forms.CharField(max_length=250, required=True, label='',
      widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter current password','label': 'Current Password'}))
    password2 = forms.CharField(max_length=250, required=True, label='',
      widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter new password','label': 'New Password'}))
    password3 = forms.CharField(max_length=250, required=True, label='',
      widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm new password','label': 'Confirm New Password'}))
 
    class Meta:
        model = User
        fields =('password1','password2','password3')
        

