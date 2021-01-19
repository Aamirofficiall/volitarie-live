from django.urls import include, path
from django.conf.urls import url
from .views import *

urlpatterns = [
    path('package/',package,name='package'),
    path('payment/<str:args>/',payment,name='payment'), 
    path('success/', success, name="success"),

]
