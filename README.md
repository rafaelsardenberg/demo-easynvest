# Demo - Easynvest

Este software foi criado em razão do processo seletivo para a vaga de Data Engineer da Easynvest.

## Visão Geral
  
O software possui as seguintes funcionalidades:<br>
  ● Processa um arquivo(retirado do site do Tesouro Nacional). Esse arquivo contém o histórico de venda e resgate dos diversos títulos do Tesouro;<br>
  ● Armazena as informações em uma base de dados SQLite;<br>
  ● Fornece APIs para manipular os títulos e suas operações.
 
## Configuração do Ambiente

Para executar o software, seguir o passo-a-passo descrito abaixo:

### Python

Obter a última versão do Python para o seu sistema operacional.

```
https://www.python.org/download/
```

### pip

O pip é o gerenciador de pacotes do Python. Siga as instruções Installing with get-pip.py no link a seguir:

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

  


