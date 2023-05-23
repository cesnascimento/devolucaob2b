from django.db import models
from app_control.utils import correios_scraper

class Devolucao(models.Model):
    codigo_sedex = models.CharField(max_length=20)
    status = models.CharField(max_length=500, null=True)
    data = models.DateTimeField(auto_now_add=True, null=True)
    email = models.CharField(max_length=20, null=True)

    def update_status(self):
        rastreio = correios_scraper(self.codigo_sedex)
        self.status = rastreio
        self.save()



class NotaDevolucao(models.Model):
    devolucao = models.ForeignKey(Devolucao, on_delete=models.CASCADE)
    nota = models.CharField(max_length=100)
