# Demo - Easynvest

Este software foi criado em razão do processo seletivo para a vaga de Data Engineer da Easynvest.

## Visão Geral
  
O software possui as seguintes funcionalidades:
* Processa um arquivo(retirado do site do Tesouro Nacional). Esse arquivo contém o histórico de venda e resgate dos diversos títulos do Tesouro;
* Armazena as informações em uma base de dados SQLite;
* Fornece APIs para manipular os títulos e suas operações.

O arquivo original do site do Tesouro Nacional está em formato .xls, o que dificulta o seu processamento. Por isso, o arquivo foi formatado para .csv, a fim de facilitar o processamento haja vista a sua padronização e também por ser de rápida leitura pelos *parses*.

O arquivo foi interpretado como três tabelas do banco de dados: Título(id, categoria), Período(id, mês, ano) e Operação(id, titulo_id, periodo_id, ação, valor). Assim, as consultas conseguem ser mais independentes e principalmente, as prováveis alterações dos dados serão menos custosas.

## Configuração do Ambiente

Requisitos:
* Python
* Django
* Django REST Framework  
  
### Python

Obter a última versão do Python para o seu sistema operacional pelo seguinte link:

```
https://www.python.org/download/
```

### pip

O pip é o gerenciador de pacotes do Python. Siga as instruções "Installing with get-pip.py" pelo seguinte link:

```
https://pip.pypa.io/en/latest/installing/
```

### Django

Na linha de comando, execute o seguinte comando:

```
pip install django
```

### Banco de Dados

O Banco de Dados SQLite já vem instalado por padrão, assim deve-se apenas executar as migrations para verificar se o banco de dados está atualizado. Para isso, execute os seguintes comandos:

```
python manage.py makemigrations app
```

```
python manage.py migrate
```

### Django REST Framework

Django REST Framework é uma ferramenta para criação de Web APIs em um ambiente Django. Para sua instalação, execute o seguinte comando:

```
pip install djangorestframework
```
Para a documentação das APIs, utiliza-se o Swagger. Para sua instalação, execute o seguinte comando:

```
pip install django-rest-swagger
```

![alt text](https://github.com/rafaelsardenberg/demo-easynvest/blob/master/swagger.PNG "Swagger")

## Servidor de Desenvolvimento

Para executar o servidor de desenvolvimento, execute o seguinte comando:

```
python manage.py runserver
```

## APIs REST:

### Títulos

#### Retornar todos os títulos

Requisição: GET /titulo/

#### Retornar todas as operações de um título

Requisição: GET /titulo/{titulo_id}/

Parâmetros: 
* data_inicio(opcional): {dd/mm/aa}
* data_fim(opcional): {dd/mm/aa}

#### Retornar todas as operações de venda de um título

Requisição: GET /titulo/{titulo_id}/vendas/

Parâmetros: 
* data_inicio(opcional): {dd/mm/aa}
* data_fim(opcional): {dd/mm/aa}

#### Retornar todas as operações de resgate de um título

Requisição: GET /titulo/{titulo_id}/resgates/

Parâmetros: 
* data_inicio(opcional): {dd/mm/aa}
* data_fim(opcional): {dd/mm/aa}

### Operações

#### Retornar todas as operações

Requisição: GET /operacao/

#### Retornar uma operação

Requisição: GET /operacao/{operacao_id}/

#### Criar ou atualizar uma operação

Requisição: POST /operacao/

Parâmetros: 
* categoria: {NTN-B, LTF, ...}
* mes: {01,02,03...}
* ano: {08,09,10,11...)
* acao: {venda, resgate}
* valor: Ponto flutuante

#### Remover uma operação

Requisição: DELETE /operacao/{operacao_id}/

#### Atualizar uma operação

Requisição: PUT /operacao/{operacao_id}/

Parâmetros: 
* valor: Ponto flutuante

### Outros

#### Importar dados do arquivo

Função utilizada para importar para o banco de dados os dados de um arquivo csv.

Requisição: GET /importar/

#### Comparar dois ou mais títulos

Requisição: GET /comparartitulos/

Parâmetros: 
* ids: [1,2,...]
* data_inicio(opcional): {dd/mm/aa}
* data_fim(opcional): {dd/mm/aa}

## Testes

Para executar os testes unitários, execute o seguinte comando:

```
python manage.py test
```

