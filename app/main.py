from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.database import create_db_and_tables
from app.routes import books

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(
    tittle='Bookstore API',
    lifespan=lifespan
)

app.include_router(books.router)

@app.get('/health')
def health_check():
    return{'status': 'ok'}