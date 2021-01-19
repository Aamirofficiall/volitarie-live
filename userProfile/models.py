from django.contrib.auth import get_user_model
from django.db import models
User = get_user_model()


class Profile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('S', 'SheMale'),
        ('O', 'Other'),
    )    
    TARGET_AUDIENCE_CHOICES = ( 
        ('S', '20-30'),
        ('M', '30-40'),
        ('B', '40-50'),
    )       
    firstName=models.CharField(max_length=30,null=True)
    lastName=models.CharField(max_length=30,null=True)
    image=models.ImageField(upload_to='Profile',null=True)
    address=models.CharField(null=True,max_length=256)
    companyEmail=models.EmailField(max_length=30,null=True)
    mobile=models.CharField(max_length=30,null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,null=True)
    dob = models.DateField(null=True) 
    job_title=models.CharField(max_length=100,null=True)
    country=models.CharField(max_length=100,null=True)
    city=models.CharField(max_length=100,null=True)
    zipcode=models.CharField(max_length=10,null=True)
    intrests=models.CharField(max_length=256,null=True)
    target_audience = models.CharField(max_length=1, choices=TARGET_AUDIENCE_CHOICES,null=True)
 
    companyName=models.CharField(max_length=256,null=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE)






