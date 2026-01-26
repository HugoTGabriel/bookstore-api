from pydantic import BaseModel
from typing import Optional

class BookCreate(BaseModel):
    title: str
    author: str
    status: str

class BookUpdate(BaseModel):
    status: Optional[str] = None