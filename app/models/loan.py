from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import date

class Loan(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    book_id: int = Field(foreign_key="book.id")
    data_emprestimo: date = Field(default_factory=date.today)
    data_devolucao_prevista: date
    data_devolucao_real: Optional[date] = None
    status: str = Field(default="ativo")