from django.urls import include, path
from django.conf.urls import url
from .views import *

urlpatterns = [
    path('settings/',index,name='setting'),


]
