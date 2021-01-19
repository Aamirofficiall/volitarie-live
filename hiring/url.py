from django.urls import include, path
from django.conf.urls import url
from .views import *

urlpatterns = [
    path('',index,name='hiring'),
    path('getHiring/', getHiringData, name='getHiringData'),
    path('getHiringByTextInput/', getHiringDataByTextInput, name='getHiringDataByTextInput'),

]
