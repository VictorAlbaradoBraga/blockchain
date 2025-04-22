from pydantic import BaseModel

# 🔒 Models de Autenticação
class UserRegister(BaseModel):
    email: str
    password: str
    name: str
    creator_type: str

class UserLogin(BaseModel):
    email: str
    password: str

# 📂 Models de Upload de Produções
class ProductionCreate(BaseModel):
    title: str
    description: str

class Production(BaseModel):
    id: str
    creator_email: str
    file_hash: str
    title: str
    description: str
    filename: str
    timestamp: int
    file_type: str

    # Converte o modelo SQLAlchemy para Pydantic
    class Config:
        orm_mode = True

# 📜 Models de Certificados
class CertificateRequest(BaseModel):
    creator_email: str
    filename: str
    file_hash: str
