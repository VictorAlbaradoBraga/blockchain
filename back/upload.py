from fastapi import APIRouter, UploadFile, File, HTTPException, Header, Form, Depends
from sqlalchemy.orm import Session
from blockchain.blockchain import Blockchain
from blockchain.transaction import Transaction
from back.utils import generate_file_hash
from back.auth import require_auth, sessions
from back.database import SessionLocal, Production
import os
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

from fastapi import Request

@router.post("/")
async def upload_file(
    request: Request,
    file: UploadFile = File(...),
    title: str = Form(...),
    description: str = Form(...),
    db: Session = Depends(get_db)
):
    print("🔔 Rota de upload foi chamada!")

    # Extrair o token do header Authorization
    auth_header = request.headers.get("authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token ausente ou inválido")

    token = auth_header.split(" ")[1]
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
        # URL para visualização da imagem
        preview_url = f"/uploads/{file.filename}"
    elif ext == ".pdf":
        file_type = "pdf"
        # URL para visualização do PDF (pode ser um ícone ou algo que indique ser um PDF)
        preview_url = "/asset/pdf.png"  # Ícone para PDF
    else:
        raise HTTPException(status_code=400, detail="Tipo de arquivo não suportado.")

    # Cria a nova produção no banco de dados
    new_production = Production(
        creator_email=email,
        file_hash=file_hash,
        title=title,
        description=description,
        filename=file.filename,
        timestamp=int(time.time()),
        file_type=file_type,
        file_url=f"/uploads/{file.filename}",  # URL do arquivo
        preview_url=preview_url  # URL da imagem de visualização
    )

    db.add(new_production)
    db.commit()
    db.refresh(new_production)  # Atualiza o objeto com os dados do banco, incluindo o ID gerado

    # Cria a transação para o blockchain
    transaction = Transaction(
        sender=email,
        recipient="blockchain_register",
        data={
            "id": new_production.id,  # Usando o ID gerado pelo banco
            "creator_email": email,
            "file_hash": file_hash,
            "title": title,
            "description": description,
            "filename": file.filename,
            "timestamp": int(time.time()),
            "file_type": file_type
        }
    )

    if blockchain.add_transaction(transaction):
        blockchain.mine_block()
        return {
            "message": "Produção registrada com sucesso.",
            "id": new_production.id,  # Retornando o ID gerado
            "file": file.filename,
            "file_url": f"/uploads/{file.filename}",  # URL do arquivo
            "preview_url": preview_url,  # URL da imagem ou ícone
            "type": file_type,
            "timestamp": int(time.time())
        }
    else:
        raise HTTPException(status_code=400, detail="Erro ao registrar produção na blockchain.")
