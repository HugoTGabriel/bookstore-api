from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.pool import StaticPool
from app.main import app
from app.core.database import get_session
from app.models.user import User
from datetime import date, timedelta
from app.models.loan import Loan
from app.models.book import Book

# 1. Motor de banco de dados INQUEBRÁVEL em memória
engine_test = create_engine(
    "sqlite://", 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool # Garante que todas as threads usem o mesmo banco de dados
)

# 2. Criar as tabelas nesse banco virtual
SQLModel.metadata.create_all(engine_test)

# 3. Interceptar a dependência
def get_session_override():
    with Session(engine_test) as session:
        yield session

app.dependency_overrides[get_session] = get_session_override

client = TestClient(app)

def test_emprestimo_estoque_zerado():
    # Setup
    with Session(engine_test) as session:
        test_user = User(nome="Aluno Teste", email="teste_isolado@bibliotech.com", senha="123")
        session.add(test_user)
        session.commit()
        session.refresh(test_user)
        user_id = test_user.id

    # Action 1: Criar livro sem estoque
    book_data = {
        "title": "Arquitetura Limpa",
        "author": "Robert C. Martin",
        "quantidade_disponivel": 0
    }
    cria_livro = client.post("/books/", json=book_data)
    assert cria_livro.status_code == 200
    livro_id = cria_livro.json()["id"]

    # Action 2: Tentar fazer o empréstimo
    loan_data = {
        "user_id": user_id,
        "book_id": livro_id,
        "dias_emprestimo": 7
    }
    response = client.post("/loans/", json=loan_data)

    # Assert: Validar a trava de segurança
    assert response.status_code == 400
    assert response.json()["detail"] == "Exemplar indisponível para empréstimo."

def test_devolucao_com_multa():
    # 1. Setup: Criar um utilizador e um livro válido para o teste de devolução
    with Session(engine_test) as session:
        test_user = User(nome="Aluno Devolucao", email="devolucao@bibliotech.com", senha="123")
        session.add(test_user)
        session.commit()
        user_id = test_user.id

    book_data = {
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "quantidade_disponivel": 1
    }
    cria_livro = client.post("/books/", json=book_data)
    livro_id = cria_livro.json()["id"]

    # 2. Setup: Forçar um empréstimo diretamente na base de dados (Viagem no tempo)
    # Vamos simular que o livro devia ter sido devolvido há 5 dias
    with Session(engine_test) as session:
        data_passada = date.today() - timedelta(days=5)
        
        # O livro sai do estoque (1 - 1 = 0)
        book = session.get(Book, livro_id)
        book.quantidade_disponivel -= 1
        
        loan_atrasado = Loan(
            user_id=user_id,
            book_id=livro_id,
            data_emprestimo=data_passada - timedelta(days=7), # Pegou há 12 dias
            data_devolucao_prevista=data_passada,             # Devia devolver há 5 dias
            status="ativo"
        )
        session.add(book)
        session.add(loan_atrasado)
        session.commit()
        session.refresh(loan_atrasado)
        loan_id = loan_atrasado.id

    # 3. Action: O Aluno tenta devolver o livro hoje
    response = client.patch(f"/loans/{loan_id}/return")

    # 4. Assert: Validar a matemática financeira e o inventário
    assert response.status_code == 200
    dados = response.json()
    assert dados["dias_atraso"] == 5
    assert dados["multa_a_pagar"] == 10.00 # 5 dias * R$ 2.00
    
    # 5. Assert: Verificar se o livro voltou para a prateleira
    check_book = client.get(f"/books/{livro_id}")
    assert check_book.json()["quantidade_disponivel"] == 1