from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class FileUpload(BaseModel):
    filename: str
    content: str  # Pode ser Base64, ou link, ou referência

class CertificateRequest(BaseModel):
    username: str
    file_id: str  # Ou o que você quiser associar
