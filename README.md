# Distributed DFS Document Search

Este projeto implementa um sistema de busca em profundidade (DFS) distribuída para encontrar um documento em um cluster de serviços usando APIs assíncronas.

## Requisitos

- Docker instalado localmente
- Separar o arquivo JSON `listingsAndReviews.json` em quantos for necessario e importar cada arquivo em seu respectivo banco de dados

## Arquivos e Estrutura

- `docker-compose.yml`: Configuração dos serviços Docker para as APIs e o MongoDB.
- `Dockerfile`: Instruções para construir a imagem Docker das APIs.
- `main.py`: Implementação do FastAPI com a busca DFS distribuída.
- `requirements.txt`: Dependências necessárias para o projeto.
- `listingsAndReviews.json`: arquivo de dados para o banco de dados.

## Teste

Acesse a pasta `\sistemasdistribuidos2` e inicie o container Docker onde serão subidos o banco de dados e os servidores, com o comando:
```docker-compose up --build -d```

Utilize em seu navegador o comando 
```http://localhost:8002/api/:ID_DESEJADO```
substituindo :ID_DESEJADO pelo id a sua escolha, caso exista o documento, o mesmo sera retornado, caso não exista retornara 'documento nao encontrado'

Após finalização dos testes 
```docker compose down```

