import hashlib
from passlib.context import CryptContext
from cryptography.fernet import Fernet

# 🔒 Gerador de senhas seguras (bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Criptografa a senha usando bcrypt."""
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    """Verifica se a senha corresponde ao hash."""
    return pwd_context.verify(password, hashed_password)

# 🔐 Gerador de chave para criptografia de arquivos
# ⚠️ Em produção, essa chave deve ser armazenada de forma segura (ex: variável de ambiente)
FERNET_KEY = Fernet.generate_key()
cipher = Fernet(FERNET_KEY)

def encrypt_content(content: bytes) -> bytes:
    """Criptografa o conteúdo do arquivo."""
    return cipher.encrypt(content)

def decrypt_content(token: bytes) -> bytes:
    """Descriptografa o conteúdo do arquivo."""
    return cipher.decrypt(token)

# 📜 Geração de Hash para Certificados
def generate_certificate_hash(data: str) -> str:
    """Gera um hash único (SHA-256) baseado nos dados do certificado."""
    return hashlib.sha256(data.encode()).hexdigest()

# 🔍 Geração de hash de arquivo para registrar na blockchain
def generate_file_hash(file_bytes: bytes) -> str:
    """Gera o hash SHA-256 de um arquivo."""
    return hashlib.sha256(file_bytes).hexdigest()
