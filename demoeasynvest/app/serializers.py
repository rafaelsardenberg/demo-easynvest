from rest_framework import serializers
from .models import Titulo,Operacao

class TituloSerializer(serializers.ModelSerializer):
	class Meta:
		model = Titulo
		fields = '__all__'	

class OperacaoSerializer(serializers.ModelSerializer):
	class Meta:
		model = Operacao
		fields = '__all__'	
