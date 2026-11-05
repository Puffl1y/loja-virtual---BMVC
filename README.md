#  Oasis – Sistema BMVC

## Sobre o projeto

O **Oasis** é um sistema web desenvolvido em Python, utilizando o framework BMVC e a biblioteca Bottle, com o objetivo de gerenciar os produtos de uma loja fictícia.

A aplicação possui dois recursos principais: **Portal**, responsável pela autenticação dos usuários, e **Banco**, destinado à visualização e ao gerenciamento dos produtos cadastrados.

## Funcionalidades

### 1. Portal
- Login e autenticação de usuários.
- Controle de acesso por sessões e cookies.
- Bloqueio de acesso ao banco para usuários não autenticados.
- Funcionalidade de logout.

### 2. Banco de produtos
- Listagem dos produtos diretamente na interface web (READ).
- Produtos com os atributos: ID, nome, categoria, preço, tamanho e cor.
- Gerenciamento dos produtos por meio de requisições CURL:
  - **CREATE (POST):** cadastro de produtos.
  - **UPDATE (PUT):** atualização de produtos.
  - **DELETE (DELETE):** exclusão de produtos.

### 3. Armazenamento de dados
Os dados são armazenados em arquivos JSON, garantindo a persistência das informações:
- `user_accounts.json`: dados dos usuários.
- `produtos.json`: produtos cadastrados.

##  Estrutura do projeto

O sistema segue a arquitetura BMVC, com separação de responsabilidades:

- **Models:** representação dos usuários e produtos.
- **Controllers:** processamento das operações e gerenciamento dos dados.
- **Views:** páginas HTML e templates da aplicação.
- **Static:** arquivos CSS e JavaScript.
- **route.py:** definição e direcionamento das rotas e requisições HTTP.

##  Tecnologias utilizadas

- Python
- Bottle
- HTML
- CSS
- JavaScript
- JSON
- CURL
- BMVC

## Recursos
- **Portal:** autenticação de usuário por formulário e cookie `session_id`.
- **Banco:** página protegida que lista os produtos cadastrados (READ).
- **API:** CREATE (`POST`), UPDATE (`PUT`) e DELETE (`DELETE`) via CURL.
- **Persistência:** `app/controllers/db/user_accounts.json` e `produtos.json`.

## Requisitos e execução
Python 3.10+ recomendado.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python route.py
```
Abra `http://localhost:8080/portal`.

Conta inicial de demonstração: `admin` / `aura123`.

## Testes CURL (Linux)
Em outro terminal, autentique e guarde o cookie da sessão:

```bash
curl -i -c cookies.txt -X POST http://localhost:8080/portal \
  -d 'username=admin' -d 'password=aura123'
```

Cadastrar (CREATE):

```bash
curl -i -b cookies.txt -X POST http://localhost:8080/api/produtos \
  -H 'Content-Type: application/json' \
  -d '{"nome":"Blusa Serena","categoria":"Blusas","preco":89.90,"tamanho":"M","cor":"Lilás"}'
```

Atualizar (UPDATE), substituindo `4` pelo ID retornado no cadastro:

```bash
curl -i -b cookies.txt -X PUT http://localhost:8080/api/produtos/4 \
  -H 'Content-Type: application/json' \
  -d '{"nome":"Blusa Serena atualizada","categoria":"Blusas","preco":94.90,"tamanho":"G","cor":"Lilás"}'
```

Excluir (DELETE), substituindo `4` pelo ID desejado:

```bash
curl -i -b cookies.txt -X DELETE http://localhost:8080/api/produtos/4
```

Depois de CREATE, UPDATE ou DELETE, atualize `/banco` no navegador para conferir a alteração. O READ exigido pela atividade está implementado na própria página `/banco`.


## Organização BMVC
- `route.py`: rotas HTTP e endpoints da API.
- `app/controllers/application.py`: controlador das páginas e autenticação.
- `app/controllers/datarecord.py`: leitura/escrita JSON, sessão e operações de produto.
- `app/models/`: modelos `UserAccount` e `Produto`.
- `app/views/html/`: templates Bottle (`portal.tpl` e `banco.tpl`).
- `app/static/css/aura.css`: identidade visual da aplicação.


## Objetivo acadêmico

O projeto foi desenvolvido como atividade prática para aplicação dos conceitos de arquitetura BMVC, desenvolvimento web, autenticação de usuários, manipulação de arquivos, APIs HTTP e operações CRUD.

A implementação contempla os requisitos propostos, incluindo autenticação no Portal, visualização dos produtos no Banco e gerenciamento por meio de requisições CURL executadas em terminal Linux.