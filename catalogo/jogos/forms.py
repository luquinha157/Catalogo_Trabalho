from django import forms
from django.shortcuts import render
from .models import Jogo

class JogoForm(forms.ModelForm):
    class Meta:
        model = Jogo
        fields = ['nome', 'imagem', 'descricao']
        widgets = {
            'imagem': forms.FileInput(attrs={'class': 'custom-input'})
        }