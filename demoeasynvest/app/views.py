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
		response = TituloSerializer(queryset, many=True).data
		return Response(response)

	def retrieve(self, request, pk=None):		
		data_inicio = formatarData(request.GET.get('data_inicio'), 1)			
		data_fim = formatarData(request.GET.get('data_fim'), 2)		
				
		titulo = Titulo.objects.filter(id = pk)[0]	
		response = {'id': pk, 'categoria': titulo.categoria}		

		historico = []
		periodos = Periodo.objects.all()
		for periodo in periodos:
			data_periodo =  int(periodo.ano+periodo.mes)
			if data_inicio <= data_periodo and data_fim >= data_periodo:			
				operacao_venda = Operacao.objects.filter(titulo_id = pk, periodo_id = periodo.id, acao = "venda")[0]
				operacao_resgate = Operacao.objects.filter(titulo_id = pk, periodo_id = periodo.id, acao = "resgate")[0]
				historico.append({'mes': periodo.mes, 'ano': periodo.ano, 'valor_venda': operacao_venda.valor, 'valor_resgate': operacao_resgate.valor})	

		response.setdefault('historico',[]).append(historico)
		return Response(response)

	@detail_route(methods=['get'])
	def vendas(self, request, pk=None):
		data_inicio = formatarData(request.GET.get('data_inicio'), 1)			
		data_fim = formatarData(request.GET.get('data_fim'), 2)	

		titulo = Titulo.objects.filter(id=pk)[0]
		response = {'id': titulo.id, 'categoria': titulo.categoria}

		valores = []
		periodos = Periodo.objects.all()
		for periodo in periodos:		
			data_periodo =  int(periodo.ano+periodo.mes)
			if data_inicio <= data_periodo and data_fim >= data_periodo:			
				valor = Operacao.objects.filter(titulo_id = pk, periodo_id = periodo.id, acao = "venda")[0].valor
				valores.append({'mes': periodo.mes, 'ano': periodo.ano, 'valor_venda': valor})

		response.setdefault('valores',[]).append(valores)
		return JsonResponse(response)

	@detail_route(methods=['get'])
	def resgates(self, request, pk=None):
		data_inicio = formatarData(request.GET.get('data_inicio'), 1)			
		data_fim = formatarData(request.GET.get('data_fim'), 2)

		titulo = Titulo.objects.filter(id=pk)[0]
		response = {'id': titulo.id, 'categoria': titulo.categoria}

		valores = []
		periodos = Periodo.objects.all()		
		for periodo in periodos:		
			data_periodo =  int(periodo.ano+periodo.mes)
			if data_inicio <= data_periodo and data_fim >= data_periodo:			
				valor = Operacao.objects.filter(titulo_id = pk, periodo_id = periodo.id, acao = "resgate")[0].valor
				valores.append({'mes': periodo.mes, 'ano': periodo.ano, 'valor_resgate': valor})

		response.setdefault('valores',[]).append(valores)
		return JsonResponse(response)

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
		response = OperacaoSerializer(queryset, many=True).data
		return Response(response)

	def retrieve(self, request, pk=None):
		queryset = Operacao.objects.filter(id=pk)
		response = OperacaoSerializer(queryset, many=True).data
		return Response(response)

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

""" Outras APIs """

def comparar(request):	
	data_inicio = formatarData(request.GET.get('data_inicio'), 1)			
	data_fim = formatarData(request.GET.get('data_fim'), 2)		
	titulos = request.GET.getlist('ids')

	response = []
	periodos = Periodo.objects.all()
	for periodo in periodos:
		data_periodo =  int(periodo.ano+periodo.mes)
		if data_inicio <= data_periodo and data_fim >= data_periodo:			
			response_aux = {'mes': periodo.mes, 'ano': periodo.ano}
			valores = []
			for titulo in titulos:
				operacao_venda = Operacao.objects.filter(titulo_id = titulo, periodo_id = periodo.id, acao="venda")[0]
				operacao_resgate = Operacao.objects.filter(titulo_id = titulo, periodo_id = periodo.id, acao="resgate")[0]
				valores.append({'titulo_id': titulo, 'valor_venda': operacao_venda.valor, 'valor_resgate': operacao_resgate.valor})
			response_aux.setdefault('valores',[]).append(valores)
			response.append(response_aux)

	return JsonResponse(response, safe=False)
	
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

	arquivo = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/dados.csv'))	
	for row in csv.reader(arquivo):
		mes = obterMes(row[1].split("-")[0])
		ano = row[1].split("-")[1]
		Periodo(id=row[0],mes=mes,ano=ano).save()				
		for i in range(2,14):			
			if(i < 8):
				Operacao(titulo_id=i-1, periodo_id=row[0], acao="venda", valor=float(row[i])).save()
			else:
				Operacao(titulo_id=i-7, periodo_id=row[0], acao="resgate", valor=float(row[i])).save()

	return Response()

""" Utils """

def formatarData(data, tipo):
	if not data and tipo == 1:
		return 0
	elif not data and tipo == 2:
		return 9999999
	else:
		mes = data.split("/")[1]
		ano = data.split("/")[2]
		return int(str(ano)+str(mes))	

def obterMes(nome):
	return {
		'jan':'01',
		'fev':'02',	
		'mar':'03',		
		'abr':'04',		
		'mai':'05',		
		'jun':'06',
		'jul':'07',
		'ago':'08',
		'set':'09',
		'out':'10',
		'nov':'11',
		'dez':'12'
	}[nome]