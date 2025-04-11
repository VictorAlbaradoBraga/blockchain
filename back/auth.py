from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from back.utils import hash_password, verify_password

# Simulando um "banco de usuários" na memória
# (depois podemos salvar na blockchain também)
users_db = {}

router = APIRouter()

class UserRegister(BaseModel):
    email: str
    password: str
    name: str
    creator_type: str  # ilustrador, designer, etc.

class UserLogin(BaseModel):
    email: str
    password: str

@router.post("/register")
def register(user: UserRegister):
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="E-mail já registrado.")

    users_db[user.email] = {
        "name": user.name,
        "creator_type": user.creator_type,
        "password": hash_password(user.password)
    }

    return {"message": "Usuário registrado com sucesso."}

@router.post("/login")
def login(user: UserLogin):
    stored_user = users_db.get(user.email)

    if not stored_user or not verify_password(user.password, stored_user["password"]):
        raise HTTPException(status_code=401, detail="E-mail ou senha inválidos.")

    return {"message": "Login realizado com sucesso."}
