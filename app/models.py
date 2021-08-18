from django.db import models
from django.contrib.auth.models import User


# https://docs.djangoproject.com/pt-br/3.2/ref/contrib/auth/#user-model
# classe User


class Receita(models.Model):
    nome = models.CharField(max_length=50)
    valor = models.FloatField()
    data = models.DateTimeField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.nome}, R$ {self.valor:.2f}'


class Despesa(models.Model):
    nome = models.CharField(max_length=50)
    valor = models.FloatField()
    data = models.DateTimeField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.nome}, R$ {self.valor:.2f}'