import uuid
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Header, Depends
from sqlalchemy.orm import Session
from back.utils import hash_password, verify_password
from back.models import UserRegister, UserLogin
from back.database import SessionLocal, User

router = APIRouter()

# Dicionário de sessões: token -> {"email": str, "expires_at": datetime}
sessions = {}

# Tempo de expiração da sessão (ex: 1 hora)
SESSION_DURATION = timedelta(hours=1)

# Dependência para pegar a sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="E-mail já registrado.")

    new_user = User(
        email=user.email,
        name=user.name,
        creator_type=user.creator_type,
        password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()

    return {"message": "Usuário registrado com sucesso."}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    stored_user = db.query(User).filter(User.email == user.email).first()

    if not stored_user or not verify_password(user.password, stored_user.password):
        raise HTTPException(status_code=401, detail="E-mail ou senha inválidos.")

    token = str(uuid.uuid4())
    sessions[token] = {
        "email": user.email,
        "expires_at": datetime.utcnow() + SESSION_DURATION
    }

    return {"token": token, "message": "Login realizado com sucesso."}

def require_auth(token: str = Header(...)):
    if not token:
        raise HTTPException(status_code=401, detail="Token não fornecido.")

    session = sessions.get(token)
    if not session:
        raise HTTPException(status_code=401, detail="Token inválido ou sessão expirada.")

    if session["expires_at"] < datetime.utcnow():
        del sessions[token]  # Remove a sessão expirada
        raise HTTPException(status_code=401, detail="Sessão expirada. Faça login novamente.")

    # Renovar tempo de expiração a cada requisição bem-sucedida
    session["expires_at"] = datetime.utcnow() + SESSION_DURATION

    return session["email"]
