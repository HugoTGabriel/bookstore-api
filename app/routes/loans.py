from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from datetime import date, timedelta
from app.core.database import get_session
from app.models.loan import Loan
from app.models.book import Book
from app.models.user import User
from app.schemas.loan import LoanCreate, LoanRead

router = APIRouter(prefix='/loans', tags=['Loans'])

@router.post('/', response_model=LoanRead)
def create_loan(loan_data: LoanCreate, session: Session = Depends(get_session)):
    # 1. Verificar se o usuário existe
    user = session.get(User, loan_data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    # 2. Verificar se o livro existe
    book = session.get(Book, loan_data.book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")

    # 3. REGRA DE NEGÓCIO: Verificação de Inventário (Proteção contra estoque negativo)
    if book.quantidade_disponivel <= 0:
        raise HTTPException(status_code=400, detail="Exemplar indisponível para empréstimo.")

    # 4. Registrar o Empréstimo
    data_prevista = date.today() + timedelta(days=loan_data.dias_emprestimo)
    
    db_loan = Loan(
        user_id=loan_data.user_id,
        book_id=loan_data.book_id,
        data_emprestimo=date.today(),
        data_devolucao_prevista=data_prevista,
        status="ativo"
    )
    
    # 5. Atualizar o Estoque do Livro
    book.quantidade_disponivel -= 1

    # 6. Salvar transação
    session.add(db_loan)
    session.add(book)
    session.commit()
    session.refresh(db_loan)
    
    return db_loan

@router.patch('/{loan_id}/return')
def return_book(loan_id: int, session: Session = Depends(get_session)):
    # 1. Buscar o empréstimo
    loan = session.get(Loan, loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Empréstimo não encontrado.")

    # 2. Impedir devolução dupla
    if loan.status == "devolvido":
        raise HTTPException(status_code=400, detail="Este livro já foi devolvido.")

    # 3. Registrar a data real de devolução
    loan.data_devolucao_real = date.today()
    
    # 4. REGRA DE NEGÓCIO: Cálculo da Multa
    multa_gerada = 0.0
    if loan.data_devolucao_real > loan.data_devolucao_prevista:
        dias_atraso = (loan.data_devolucao_real - loan.data_devolucao_prevista).days
        taxa_diaria = 2.00
        multa_gerada = dias_atraso * taxa_diaria
    
    # 5. Atualizar status do empréstimo
    loan.status = "devolvido"

    # 6. Devolver o livro para a prateleira (Inventário)
    book = session.get(Book, loan.book_id)
    if book:
        book.quantidade_disponivel += 1
        session.add(book)

    # 7. Salvar e consolidar a transação
    session.add(loan)
    session.commit()
    session.refresh(loan)

    return {
        "mensagem": "Devolução realizada com sucesso.",
        "loan_id": loan.id,
        "dias_atraso": dias_atraso if multa_gerada > 0 else 0,
        "multa_a_pagar": round(multa_gerada, 2)
    }

@router.patch('/{loan_id}/return')
def return_book(loan_id: int, session: Session = Depends(get_session)):
    # 1. Procurar o registo do empréstimo
    loan = session.get(Loan, loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Empréstimo não encontrado.")

    # 2. Impedir fraude de devolução dupla (que geraria inventário infinito)
    if loan.status == "devolvido":
        raise HTTPException(status_code=400, detail="Este exemplar já foi devolvido.")

    # 3. Marcar o momento real
    loan.data_devolucao_real = date.today()
    
    # 4. REGRA DE NEGÓCIO: Cálculo de Atraso e Multa
    multa_gerada = 0.0
    dias_atraso = 0
    if loan.data_devolucao_real > loan.data_devolucao_prevista:
        dias_atraso = (loan.data_devolucao_real - loan.data_devolucao_prevista).days
        taxa_diaria = 2.00 # R$ 2.00 por dia
        multa_gerada = dias_atraso * taxa_diaria
    
    # 5. Atualizar o estado da transação
    loan.status = "devolvido"

    # 6. REGRA DE NEGÓCIO: Reposição de Inventário
    book = session.get(Book, loan.book_id)
    if book:
        book.quantidade_disponivel += 1
        session.add(book)

    # 7. Consolidar na base de dados
    session.add(loan)
    session.commit()
    session.refresh(loan)

    return {
        "mensagem": "Devolução realizada com sucesso.",
        "loan_id": loan.id,
        "dias_atraso": dias_atraso,
        "multa_a_pagar": round(multa_gerada, 2)
    }