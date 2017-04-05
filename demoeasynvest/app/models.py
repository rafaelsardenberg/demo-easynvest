from django.db import models

class Titulo(models.Model):
	id = models.IntegerField(primary_key=True)
	categoria = models.CharField(max_length=255)	

class Periodo(models.Model):
	id = models.IntegerField(primary_key=True)
	mes = models.CharField(max_length=255)
	ano = models.CharField(max_length=255)

class Operacao(models.Model):
	id = models.AutoField(primary_key=True)
	titulo_id = models.IntegerField(default=0)
	periodo_id = models.IntegerField(default=0)
	acao = models.CharField(max_length=255)
	valor = models.FloatField(default=0)