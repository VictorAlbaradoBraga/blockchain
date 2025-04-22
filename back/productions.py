from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from back.database import SessionLocal, Production
from back.models import Production as ProductionModel
from back.auth import require_auth  # <-- IMPORTANTE

router = APIRouter()

# Dependência para pegar a sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/list", response_model=list[ProductionModel])
def list_productions(db: Session = Depends(get_db)):
    productions = db.query(Production).all()
    return productions

@router.get("/my-list", response_model=list[ProductionModel])
def list_my_productions(token: str = Header(...), db: Session = Depends(get_db)):
    email = require_auth(token)
    productions = db.query(Production).filter(Production.creator_email == email).all()
    return productions
