from fastapi import HTTPException
from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from typing import Optional
from app.schemas.book import BookCreate
from app.schemas.book import BookUpdate
from app.models.book import Book
from app.core.database import  get_session

router = APIRouter(prefix='/books', tags=['Books'])

@router.post('/')
def creat_book(book: BookCreate, session: Session = Depends(get_session)):
    db_book = Book(
        title=book.title,
        author=book.author,
        quantidade_disponivel=book.quantidade_disponivel 
    )
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book

@router.get('/')
def list_books(
    status: Optional[str] = None,
    session: Session = Depends(get_session)
):
    statement = select(Book)
    if status:
        statement = statement.where(Book.status == status)
    books = session.exec(statement).all()
    return books

@router.get("/{book_id}")
def get_book(book_id: int, session: Session = Depends(get_session)):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.delete('/{book_id}', status_code=204)
def delete_book(book_id: int, session: Session = Depends(get_session)):
    book = session.get(Book, book_id)

    if not book:
        raise HTTPException(status_code=404, detail='Book not found')
    
    session.delete(book)
    session.commit()

@router.put('/{book_id}')
def update_book(
    book_id: int,
    updated_book: Book,
    session: Session = Depends(get_session)
):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail='Book not found')
    book.title = updated_book.title
    book.author = updated_book.author
    book.status = updated_book.status
    session.add(book)
    session.commit()
    session.refresh(book)
    return book
