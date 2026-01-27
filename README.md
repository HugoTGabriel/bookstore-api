📚 Book Tracker API

API REST desenvolvida com FastAPI para gerenciar livros e acompanhar o status de leitura (não lido, lendo, lido).
Este projeto foi criado com foco em aprendizado prático de backend, incluindo CRUD completo, filtros, boas práticas de arquitetura e integração com banco de dados.

🚀 Funcionalidades

Criar livros
Listar todos os livros
Buscar livro por ID
Atualizar livro (PUT)
Atualizar apenas o status de leitura (PATCH)
Remover livros
Filtrar livros por status (lido, lendo, nao_lido)

🛠️ Tecnologias utilizadas

Python 3
FastAPI
SQLModel
SQLite
Git / GitHub

▶️ Como rodar o projeto localmente

git clone https://github.com/SEU_USUARIO/bookstore-api.git
cd bookstore-api
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload

Acesse: http://127.0.0.1:8000/docs

📌 Exemplos de uso

Criar um livro

POST /books
{
  "title": "1984",
  "author": "George Orwell",
  "status": "lendo"
}

Filtrar por status
GET /books?status=lendo

📈 Próximos passos (roadmap)

Interface web simples para consumo da API
Autenticação de usuários
Vínculo de livros por usuário

🧠 Aprendizados

CRUD completo com FastAPI
Diferença entre PUT e PATCH
Injeção de dependência (Depends)
Modelagem de dados com SQLModel
Filtros via query params
Versionamento com Git
