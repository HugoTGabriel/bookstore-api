# 📚 Book Tracker API

API REST desenvolvida com **FastAPI** para gerenciar livros e acompanhar o status de leitura  
(**não lido**, **lendo**, **lido**).

Este projeto foi criado com foco em **aprendizado prático de backend**, aplicando conceitos reais
como CRUD completo, filtros, boas práticas de arquitetura e integração com banco de dados.

---

## 🚀 Funcionalidades

- Criar livros
- Listar todos os livros
- Buscar livro por ID
- Atualizar livro completo (**PUT**)
- Atualizar apenas o status de leitura (**PATCH**)
- Remover livros
- Filtrar livros por status:
  - `lido`
  - `lendo`
  - `nao_lido`

---

## 🛠️ Tecnologias utilizadas

- Python 3
- FastAPI
- SQLModel
- SQLite
- Git / GitHub

---

## ▶️ Como rodar o projeto localmente

```bash
git clone https://github.com/SEU_USUARIO/bookstore-api.git
cd bookstore-api
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Após iniciar o servidor, a API ficará disponível localmente.
