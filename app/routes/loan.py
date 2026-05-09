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