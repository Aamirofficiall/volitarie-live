from django.conf.urls import url
from .views import *
from django.urls import include, path
urlpatterns = [
    
    path('connect/',connect ,name='connect'),
    url('profile/',profile ,name='profile'),
    path('',home ,name='home'),


]