from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome


class Conta(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='contas'
    )
    nome = models.CharField(max_length=100)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='contas'
    )

    def __str__(self):
        return self.nome
