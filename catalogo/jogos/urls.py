from django.urls import path
from jogos.views import *

urlpatterns = [
    path('', index, name='index'),
]