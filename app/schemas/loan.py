from pydantic import BaseModel
from datetime import date
from typing import Optional

class LoanCreate(BaseModel):
    user_id: int
    book_id: int
    dias_emprestimo: int = 7 

class LoanRead(BaseModel):
    id: int
    user_id: int
    book_id: int
    data_emprestimo: date
    data_devolucao_prevista: date
    status: str