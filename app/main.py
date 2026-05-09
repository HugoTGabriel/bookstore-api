from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import create_db_and_tables
from app.routes import books
from app.models import book, user, loan
from app.routes import books, loans

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(
    title='BiblioTech API', 
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. REGISTRO DOS ROUTERS
app.include_router(books.router)
app.include_router(loans.router)

@app.get('/health')
def health_check():
    return {'status': 'ok', 'system': 'BiblioTech'}