# 📚 Book Tracker API

API REST desenvolvida com **FastAPI** para gerenciar livros e acompanhar o status de leitura (**lendo**, **lido**, **pendente**), acompanhada de uma **interface web simples em HTML, CSS e JavaScript puro**.

Este projeto foi criado com foco em **aprendizado prático de backend**, integração com frontend, arquitetura organizada e boas práticas de APIs REST.

---

## 🚀 Funcionalidades

### 📖 Backend (API)
- Criar livros
- Listar todos os livros
- Buscar livro por ID
- Atualizar livro completo (PUT)
- Atualizar apenas o status de leitura (PATCH)
- Remover livros
- Filtrar livros por status (`lido`, `lendo`, `pendente`)
- Banco de dados relacional com SQLite
- Documentação automática via Swagger (`/docs`)

### 🖥️ Frontend
- Interface web simples e funcional
- Listagem dinâmica de livros
- Criação de livros via formulário
- Botões rápidos para atualizar status
- Remoção de livros em tempo real
- Atualização visual por cor de status
- Integração completa com a API via `fetch`

---

## 🎨 Status e Cores

| Status     | Cor |
|------------|-----|
| Lendo      | 🟡 Amarelo |
| Lido       | 🟢 Verde |
| Pendente   | 🔴 Vermelho |

---

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3**
- **FastAPI**
- **SQLModel**
- **SQLite**
- **Uvicorn**
- **CORS Middleware**

### Frontend
- **HTML5**
- **CSS3**
- **JavaScript (Vanilla JS)**

### Ferramentas
- **Git & GitHub**
- **VS Code**
