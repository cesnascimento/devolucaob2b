from django.db import models
from app_control.utils import correios_postagem, correios_sedex
from django.utils import timezone

class Devolucao(models.Model):
    codigo_postagem = models.CharField(max_length=500, unique=True, null=True,  error_messages={
        'unique': 'Este código já existe',
    })
    codigo_sedex = models.CharField(max_length=500, error_messages={
        'unique': 'Este código já existe',
    })
    status = models.CharField(max_length=500, null=True)
    data = models.DateTimeField(null=True)
    email = models.CharField(max_length=500, null=True)

    def update_status(self):
        rastreio = correios_postagem(self.codigo_postagem)
        sedex = correios_sedex(rastreio)
        self.status = sedex
        self.codigo_sedex = rastreio
        self.save()



class NotaDevolucao(models.Model):
    devolucao = models.ForeignKey(Devolucao, on_delete=models.CASCADE)
    nota = models.CharField(max_length=100)
