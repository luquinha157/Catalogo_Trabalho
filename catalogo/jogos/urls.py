from django.urls import path
from jogos.views import *

urlpatterns = [
    path('', index, name='index'),
    path('login', login, name='login'),
    path('cadastro', register, name='cadastro'),
    path('logout', logout, name='logout'),
    path('dashboard/users', index, name="users"),
    path('inativar/<int:id>', inative, name="inative_user"),
    path('ativar/<int:id>', active, name="active_user"),
    path('dashboard', dashboard, name="dashboard"),
    path('add_jogos', add_jogos, name="add_jogos"),
]