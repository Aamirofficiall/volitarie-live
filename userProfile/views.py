from django.contrib.auth.decorators import login_required 

from django.shortcuts import render,HttpResponse
from .models import *
from .forms import *

@login_required(login_url='login')
def profile(request):
    try:
        profile=Profile.objects.get_or_create(user=request.user)
    except:
        return HttpResponse('<h1> 404 Not Found </h>')

    profile=Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(instance=profile, data=request.POST)
        if form.is_valid():
            form.save()
    form = ProfileForm(instance=profile)
    return render(request,'profile.html',{'form':form})


def connect(request,id):
    return render(request,'connect.html',{'form':form})

def home(request):
    return render(request,'home.html')
    