from django.test import TestCase
from rest_framework.test import RequestsClient
from rest_framework.test import APITestCase
from app.models import Operacao, Titulo, Periodo

class APITests(APITestCase):
	def test_list_operacao(self):
		Operacao(titulo_id=1, periodo_id=1, acao="venda", valor=1.0).save()
		client = RequestsClient()
		response = client.get('http://127.0.0.1:8000/operacao/')
		assert response.status_code == 200

	def test_create_operacao(self):
		Titulo(id=1,categoria='Teste').save()
		Periodo(id=1,mes=1,ano=6).save()			
		client = RequestsClient()
		client.post('http://127.0.0.1:8000/operacao/?categoria=Teste&acao=venda&mes=1&ano=6&valor=100')		
		assert Operacao.objects.all().count() == 1

	def test_update_operacao(self):
		Operacao(titulo_id=1, periodo_id=1, acao="venda", valor=1).save()
		operacao_id = Operacao.objects.all()[0].id		
		client = RequestsClient()
		client.put('http://127.0.0.1:8000/operacao/' + str(operacao_id) + '/?valor=100')		
		assert Operacao.objects.all()[0].valor == 100

	def test_delete_operacao(self):
		Operacao(titulo_id=1, periodo_id=1, acao="venda", valor=1.0).save()		
		operacao_id = Operacao.objects.all()[0].id		
		client = RequestsClient()
		client.delete('http://127.0.0.1:8000/operacao/' + str(operacao_id))	
		assert Operacao.objects.all().count() == 0