from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Empresa(models.Model):
    abertura = models.DateField()
    situacao = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)
    nome = models.CharField(max_length=100)
    fantasia = models.CharField(max_length=100, null=True, blank=True)
    endereco = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=14, unique=True)
    email = models.EmailField()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
