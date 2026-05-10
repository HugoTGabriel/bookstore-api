from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.user import User
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix='/users', tags=['Users'])

# Schema para entrada (o que o usuário envia)
class UserCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str

# Schema para saída (o que a API responde - SEM A SENHA)
class UserRead(BaseModel):
    id: int
    nome: str
    email: str

@router.post('/', response_model=UserRead)
def create_user(user_data: UserCreate, session: Session = Depends(get_session)):
    # 1. Verificar se o e-mail já está em uso
    statement = select(User).where(User.email == user_data.email)
    existing_user = session.exec(statement).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Este e-mail já está cadastrado.")

    # 2. CUIDADO: Aqui você deveria aplicar o Hashing (ex: pwd_context.hash(user_data.senha))
    # Para fins de Ciclo 2, vamos manter a lógica mas você DEVE saber que salvar puro é erro técnico.
    db_user = User(
        nome=user_data.nome,
        email=user_data.email,
        senha=user_data.senha  # Ponto cego estratégico: substitua por hash no futuro
    )
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user