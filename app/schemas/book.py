from pydantic import BaseModel
from typing import Optional

class BookCreate(BaseModel):
    title: str
    author: str
    quantidade_disponivel: int = 1

class BookUpdate(BaseModel):
    quantidade_disponivel: Optional[int] = None