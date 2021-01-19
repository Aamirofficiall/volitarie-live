from django.urls import include, path
from django.conf.urls import url
from .views import *

urlpatterns = [
    path('', index, name='linkdin'),
    path('getLinkdin/', getLinkdinData, name='get-linkdin'),
]
