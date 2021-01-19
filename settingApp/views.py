from django.shortcuts import render,redirect
from .forms import *
from django.core.exceptions import ValidationError

from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def index(request):
    updateForm =UpdateUserForm(instance=request.user)
    updatePassForm = UpdateUserPasswordForm()

    flag= 'form1'
    if request.method=='POST':
        updateForm =UpdateUserForm(instance=request.user,data=request.POST)
        updatePassForm = UpdateUserPasswordForm(data=request.POST)        
        if request.POST.get('form_type') == 'form1':
            email=request.POST.get('email')
            flag= 'form1'
            updateForm=UpdateUserForm(instance=request.user,data=request.POST)
            if User.objects.filter(email=email).count()  >= 1 and request.user.email !=email:
                updateForm.add_error("email",error= ValidationError("User already exist with this email"))
                return render(request,'userSettings.html',{'updateForm':updateForm,'updatePassForm':updatePassForm,'flag':flag})        
            email=request.POST.get('email')    
            if updateForm.is_valid():
                updateForm.save()
            
                
        if request.POST.get('form_type') == 'form2':
            print('second form')
            flag= ''
            password1=request.POST.get('password1')
            password2=request.POST.get('password2')
            password3=request.POST.get('password3')
            print(password1)
            if request.user.check_password(password1):
                print('in')
                if password2 == password3:
                    request.user.set_password(password1)
                    request.user.save()
                else:
                    updatePassForm.add_error("password2",error= ValidationError("New password didn't match"))

            else:
                    print('her i m')
                    updatePassForm.add_error("password1",error= ValidationError("Current password didn't match"))

    return render(request,'userSettings.html',{'updateForm':updateForm,'updatePassForm':updatePassForm,'flag':flag})

