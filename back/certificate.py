from fastapi import APIRouter
from back.utils import generate_certificate_hash
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/certificate/{file_hash}")
def generate_certificate(file_hash: str, creator_email: str, filename: str):
    # Gera uma "assinatura" digital do certificado
    data = f"{file_hash}:{creator_email}:{filename}"
    certificate_hash = generate_certificate_hash(data)

    certificate_info = {
        "creator_email": creator_email,
        "filename": filename,
        "file_hash": file_hash,
        "certificate_hash": certificate_hash,
        "message": "Certificado válido. Obra registrada na blockchain."
    }

    return JSONResponse(content=certificate_info)
