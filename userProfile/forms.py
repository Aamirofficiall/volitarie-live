from django.contrib.auth import get_user_model
from django import forms
from .models import *
User = get_user_model()


class DateInput(forms.DateInput):
    input_type = 'date'

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user','id')
        widgets = {
            'firstName':forms.TextInput(attrs={"class":"form-control" , 'placeholder': 'Enter your first name','required':False}),
            'lastName':forms.TextInput(attrs={"class":"form-control" , 'placeholder': 'Enter your last name'}),
            'companyEmail':forms.TextInput(attrs={"class":"form-control" , 'placeholder': 'Add your Company email'}),
            'companyName': forms.TextInput(attrs={"class":"form-control" , 'placeholder': 'Enter Your Company name'}) ,
            'address':forms.TextInput(attrs={"class":"form-control", 'placeholder': 'Enter your Address'}) , 
            'mobile':forms.TextInput(attrs={"class":"form-control", 'placeholder': 'Enter your Mobile Number'}) , 
            'zipcode':forms.TextInput(attrs={"class":"form-control", 'placeholder': 'Enter ZipCode'}) , 
            'country':forms.TextInput(attrs={"class":"form-control", 'placeholder': 'Enter your Country'}) , 
            'city':forms.TextInput(attrs={"class":"form-control", 'placeholder': 'Enter your City'}) , 
            'intrests':forms.TextInput(attrs={"class":"form-control", 'placeholder': 'Enter your Intrests'}) , 
            'dob': DateInput() 
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['firstName'].required = False
        self.fields['lastName'].required = False
        self.fields['companyEmail'].required = False
        self.fields['companyName'].required = False 
        self.fields['address'].required = False
        self.fields['mobile'].required = False
        self.fields['zipcode'].required = False
        self.fields['country'].required = False
        self.fields['city'].required = False
        self.fields['intrests'].required = False
        self.fields['gender'].required = False
        self.fields['target_audience'].required = False 
        self.fields['dob'].required = False 


