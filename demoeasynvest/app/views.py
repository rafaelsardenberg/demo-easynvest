import os,csv
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from app.serializers import TituloSerializer, OperacaoSerializer
from app.models import Titulo, Periodo, Operacao

class TituloViewSet(viewsets.ViewSet):
	"""
	list:
   	Retorna todos os títulos
    retrieve:
    Retorna todas as operações de um título
    vendas:
    Retorna todas as operações de venda de um título
    resgates:
    Retorna todas as operações de resgate de um título  
    """

	def list(self, request):
		queryset = Titulo.objects.all()
		serializer = TituloSerializer(queryset, many=True)
		return Response(serializer.data)

	def retrieve(self, request, pk=None):
		historico = []	
		titulo = Titulo.objects.filter(id = pk)[0]	
		toReturn = {'id': pk, 'categoria': titulo.categoria}		
		periodos = Periodo.objects.all()
		for periodo in periodos:
			operacao_venda = Operacao.objects.filter(titulo_id = pk, periodo_id = periodo.id, acao = "venda")[0]
			operacao_resgate = Operacao.objects.filter(titulo_id = pk, periodo_id = periodo.id, acao = "resgate")[0]
			historico.append({'mes': periodo.mes, 'ano': periodo.ano, 'valor_venda': operacao_venda.valor, 'valor_resgate': operacao_resgate.valor})

		toReturn.setdefault('historico',[]).append(historico)
		return Response(toReturn)

	@detail_route(methods=['get'])
	def vendas(self, request, pk=None):
		t = Titulo.objects.filter(id=pk)[0]
		toReturn = {'id': t.id, 'categoria': t.categoria}
		periodos = Periodo.objects.all()
		valores = []
		for periodo in periodos:		
			valor = Operacao.objects.filter(titulo_id = pk, periodo_id = periodo.id, acao = "venda")[0].valor
			valores.append({'mes': periodo.mes, 'ano': periodo.ano, 'valor_venda': valor})

		toReturn.setdefault('valores',[]).append(valores)
		return JsonResponse(toReturn)

	@detail_route(methods=['get'])
	def resgates(self, request, pk=None):
		t = Titulo.objects.filter(id=pk)[0]
		toReturn = {'id': t.id, 'categoria': t.categoria}
		periodos = Periodo.objects.all()
		valores = []
		for periodo in periodos:		
			valor = Operacao.objects.filter(titulo_id = pk, periodo_id = periodo.id, acao = "resgate")[0].valor
			valores.append({'mes': periodo.mes, 'ano': periodo.ano, 'valor_resgate': valor})

		toReturn.setdefault('valores',[]).append(valores)
		return JsonResponse(toReturn)

class OperacaoViewSet(viewsets.ViewSet):
	"""
	list:
   	Retorna todas as operações
    retrieve:
    Retorna uma operação
    create:
    Cria ou atualiza uma operação
    update:
    Atualiza uma operação
    destroy:
    Remove uma operação
    """

	def list(self, request):
		queryset = Operacao.objects.all()
		serializer = OperacaoSerializer(queryset, many=True)
		return Response(serializer.data)

	def retrieve(self, request, pk=None):
		queryset = Operacao.objects.filter(id=pk)
		serializer = OperacaoSerializer(queryset, many=True)
		return Response(serializer.data)

	def create(self, request):
		categoria_req = request.GET.get('categoria')		
		acao_req = request.GET.get('acao')			
		mes_req	= request.GET.get('mes')			
		ano_req	= request.GET.get('ano')		
		valor_req = request.GET.get('valor')		
		titulo_id = Titulo.objects.filter(categoria=categoria_req)[0].id
		periodo_id = Periodo.objects.filter(mes=mes_req,ano=ano_req)[0].id

		"""Verifica se já existe uma operação com esses dados"""
		if Operacao.objects.filter(titulo_id=titulo_id, periodo_id=periodo_id, acao=acao_req).count() > 0:
			operacao = Operacao.objects.filter(titulo_id=titulo_id, periodo_id=periodo_id, acao=acao_req)[0]
			operacao.valor = valor_req
			operacao.save()
		else:
			Operacao(titulo_id=titulo_id, periodo_id=periodo_id, acao=acao_req, valor=valor_req).save()		
		return Response()

	def update(self, request, pk=None):	
		valor_req = request.GET.get('valor')
		operacao = Operacao.objects.filter(id=pk)[0]		
		operacao.valor = valor_req
		operacao.save()		
		return Response()

	def destroy(self, request, pk=None):
		Operacao.objects.filter(id=pk).delete()		
		return Response()

def comparar(request):	
	titulos = request.GET.getlist('ids')
	periodos = Periodo.objects.all()
	toReturn = []
	for periodo in periodos:
		toReturnAux = {'mes': periodo.mes, 'ano': periodo.ano}
		valores = []
		for titulo in titulos:
			operacao_venda = Operacao.objects.filter(titulo_id = titulo, periodo_id = periodo.id, acao="venda")[0]
			operacao_resgate = Operacao.objects.filter(titulo_id = titulo, periodo_id = periodo.id, acao="resgate")[0]
			valores.append({'titulo_id': titulo, 'valor_venda': operacao_venda.valor, 'valor_resgate': operacao_resgate.valor})
		toReturnAux.setdefault('valores',[]).append(valores)
		toReturn.append(toReturnAux)
	return JsonResponse(toReturn, safe=False)
	
def importar(request):	
	Titulo.objects.all().delete()
	Periodo.objects.all().delete()
	Operacao.objects.all().delete()
	Titulo(id=1,categoria="LTN").save()
	Titulo(id=2,categoria="LFT").save()
	Titulo(id=3,categoria="NTN-B").save()
	Titulo(id=4,categoria="NTN-B Principal").save()
	Titulo(id=5,categoria="NTN-C").save()
	Titulo(id=6,categoria="NTN-F").save()

	f = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/dados.csv'))	
	for row in csv.reader(f):
		mes = obterMes(row[1].split("-")[0])
		ano = int(row[1].split("-")[1])
		Periodo(id=row[0],mes=mes,ano=ano).save()				
		for i in range(2,14):			
			if(i < 8):
				Operacao(titulo_id=i-1, periodo_id=row[0], acao="venda", valor=float(row[i])).save()
			else:
				Operacao(titulo_id=i-7, periodo_id=row[0], acao="resgate", valor=float(row[i])).save()

	return Response()

def obterMes(nome):
	return {
		'jan':1,
		'fev':2,	
		'mar':3,		
		'abr':4,		
		'mai':5,		
		'jun':6,
		'jul':7,
		'ago':8,
		'set':9,
		'out':10,
		'nov':11,
		'dez':12
	}[nome]