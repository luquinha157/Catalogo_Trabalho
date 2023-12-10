from django.db import models

# Create your models here.

class Jogo(models.Model):
    nome = models.CharField(max_length=20)
    imagem = models.ImageField(upload_to='media/')
    descricao = models.TextField(max_length=150)

    def __str__(self):
        return self.nome