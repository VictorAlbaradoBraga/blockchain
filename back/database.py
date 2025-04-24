from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./users.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    email = Column(String, primary_key=True, index=True)
    name = Column(String)
    creator_type = Column(String)
    password = Column(String)

class Production(Base):
    __tablename__ = "productions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)  # Alterado para Integer e autoincrement
    creator_email = Column(String)
    file_hash = Column(String)
    title = Column(String)
    description = Column(String)
    filename = Column(String)
    timestamp = Column(Integer)
    file_type = Column(String)
    file_url = Column(String)
    preview_url = Column(String)


# Cria o banco se não existir
Base.metadata.create_all(bind=engine)
