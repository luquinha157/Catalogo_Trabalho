from django.urls import path
from jogos.views import *

urlpatterns = [
    path('', index, name='index'),
    path('listar/', listar_produtos, name='listar_produtos'),
]