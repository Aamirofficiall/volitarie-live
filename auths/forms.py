from django import forms
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.forms import UserCreationForm,UserChangeForm

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email', 'password1', 'password2']
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email'        
        self.fields['username'].widget.attrs['placeholder'] = 'Enter Username'        
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter Password'        
        self.fields['password2'].widget.attrs['placeholder'] = 'Re-Enter Password'        

class UpdateUserForm(UserChangeForm):
    first_name = forms.CharField(max_length=250, required=True, label='',
      widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=250, required=True, label='',
      widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    # username = forms.CharField(max_length=250, required=True, label='',
    #   widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    email = forms.EmailField(max_length=250, required=True, label='',
      widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name','username', 'email',)

class LoginForm(forms.Form):
    email = forms.CharField(max_length=254, help_text='Required. Inform a valid email address.',
        widget = forms.EmailInput(attrs={'class':'form-control' , "placeholder":"Email Address"})
    )
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', "class" : "form-control", "placeholder":"Password"}),
        
    )
