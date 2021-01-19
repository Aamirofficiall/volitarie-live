from django.shortcuts import render,HttpResponseRedirect,redirect
from django.contrib.auth import authenticate, login , logout
from django.template.defaultfilters import slugify
from django.forms import ValidationError
from django.contrib import messages
from userProfile.models import *
from .forms import * 

def register(request):

    if (request.method == 'POST'):
        form = RegisterForm(request.POST)
        # companyName=request.POST.get('companyName')
        firstName=request.POST.get('firstName')
        lastName=request.POST.get('lastName')

        if form.is_valid(): 
            user=form.save()
            profile=Profile.objects.create(
                user=user,
                # companyName=companyName,
                firstName=firstName,
                lastName=lastName)
                
            profile.save()
            messages.success(request, 'Registration has been done Successfully for "'+user.email+'"')
            return redirect('login')
        else:
            return render(request, 'register.html',{'form': form})

    return render(request, 'register.html',{'form': RegisterForm()}) 

def loginView(request):
    """
        
        This function will handle user login functionality to kompetez 
        website for normal user.

        It will check email first ,weather it exist in database and match
        it with existing emails if it doesn't exist it will show an error message.

    """
    form = LoginForm(request.POST)
    if (request.method == 'POST'):
        email = request.POST.get('email')  #Get email value from form
        password = request.POST.get('password') #Get password value from form
        
        user = authenticate(request, email=email, password=password)
     
        if User.objects.filter(email=email).count() < 1:
            form.add_error("email",error= ValidationError("No User Found with the Credentials"))
            return render(request, 'login.html', {'form': form })
          
        if user is not None:
            
            login(request, user)
            next_url = request.GET.get('next')
            if next_url:
                return HttpResponseRedirect(next_url)
            else:
                return redirect('home')
  

        else:
            form.add_error("email",error= ValidationError("Password Missmatch!"))
        return render(request, 'login.html', {'form': form })
    return render(request, 'login.html',{'form': LoginForm() })
