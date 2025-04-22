from fastapi import APIRouter, UploadFile, File, HTTPException, Header, Form, Depends
from sqlalchemy.orm import Session
from blockchain.blockchain import Blockchain
from blockchain.transaction import Transaction
from back.utils import generate_file_hash
from back.auth import require_auth, sessions
from back.database import SessionLocal, Production
import os
import uuid
import time

router = APIRouter()

blockchain = Blockchain()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Dependência para pegar a sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
async def upload_file(
    file: UploadFile = File(...),
    title: str = Form(...),
    description: str = Form(...),
    token: str = Header(...),
    db: Session = Depends(get_db)
):
    email = require_auth(token)

    # Verifica se o arquivo foi enviado
    if not file:
        raise HTTPException(status_code=400, detail="Arquivo inválido.")

    # Lê o conteúdo do arquivo
    file_bytes = await file.read()
    file_hash = generate_file_hash(file_bytes)

    # Salva o arquivo no diretório de upload
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(file_bytes)

    # Verifica a extensão do arquivo
    ext = os.path.splitext(file.filename)[1].lower()
    if ext in [".png", ".jpg", ".jpeg", ".gif"]:
        file_type = "image"
    elif ext == ".pdf":
        file_type = "pdf"
    else:
        raise HTTPException(status_code=400, detail="Tipo de arquivo não suportado.")

    # Cria um novo ID para a produção
    production_id = str(uuid.uuid4())

    # Cria a nova produção no banco de dados
    new_production = Production(
        creator_email=email,
        file_hash=file_hash,
        title=title,
        description=description,
        filename=file.filename,
        timestamp=int(time.time()),
        file_type=file_type
    )

    db.add(new_production)
    db.commit()

    # Cria a transação para o blockchain
    transaction = Transaction(
        sender=email,
        recipient="blockchain_register",
        data={
            "id": production_id,
            "creator_email": email,
            "file_hash": file_hash,
            "title": title,
            "description": description,
            "filename": file.filename,
            "timestamp": int(time.time()),
            "file_type": file_type
        }
    )

    # Registra a transação no blockchain
    if blockchain.add_transaction(transaction):
        blockchain.mine_block()
        return {
            "message": "Produção registrada com sucesso.",
            "id": production_id,
            "file": file.filename,
            "type": file_type,
            "timestamp": int(time.time())
        }
    else:
        raise HTTPException(status_code=400, detail="Erro ao registrar produção.")
