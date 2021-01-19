from django.urls import include, path
from django.conf.urls import url
from .views import *

urlpatterns = [
    path('', index, name='competition'),
    path('getCompetition/', getCompetitionData, name='getCompetitionData'),
]
