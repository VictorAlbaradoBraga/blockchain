from fastapi import APIRouter, UploadFile, File, HTTPException
from blockchain.blockchain import Blockchain
from blockchain.transaction import Transaction
from back.utils import generate_file_hash, encrypt_content
import time

router = APIRouter()

# Instancia uma blockchain
blockchain = Blockchain()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...), creator_email: str = ""):
    if not file:
        raise HTTPException(status_code=400, detail="Arquivo inválido.")

    # Leitura e hash do arquivo
    file_bytes = await file.read()
    file_hash = generate_file_hash(file_bytes)

    # Opcional: criptografar o conteúdo antes de salvar (proteção extra)
    encrypted_content = encrypt_content(file_bytes)

    # Criar uma transação com os dados da obra
    transaction = Transaction(
        sender=creator_email,
        recipient="blockchain_register",
        data={
            "filename": file.filename,
            "file_hash": file_hash,
            "timestamp": int(time.time()),
            "creator_email": creator_email
        }
    )

    if blockchain.add_transaction(transaction):
        blockchain.mine_block()
        return {
            "message": "Arquivo registrado com sucesso.",
            "file_hash": file_hash
        }
    else:
        raise HTTPException(status_code=400, detail="Erro ao registrar o arquivo.")
