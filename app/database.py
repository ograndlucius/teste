# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

# Função de dependência para obter uma sessão do banco de dados.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# URL do banco de dados SQLite. O banco será criado no diretório atual.
DATABASE_URL = "sqlite:///./test.db"

# Criação de uma instância do mecanismo SQLAlchemy para interagir com o banco de dados.
engine = create_engine(DATABASE_URL)

# Criação de uma fábrica de sessões para interagir com o banco de dados.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# DeclarativeBase é uma classe base para a definição de modelos SQLAlchemy.
Base = declarative_base()
