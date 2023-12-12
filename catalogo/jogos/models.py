from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Jogo(models.Model):
    nome = models.CharField(max_length=20)
    imagem = models.ImageField(upload_to='media/')
    descricao = models.TextField(max_length=50)

    def __str__(self):
        return self.nome