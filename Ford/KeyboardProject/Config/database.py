"""
database
--------
Configuração central da conexão com o banco de dados: engine,
fábrica de sessões e a Base declarativa usada pelos models ORM.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Ajuste usuário/senha/host/porta conforme o seu docker-compose.yml.
# Rodando FORA do Docker (na sua máquina Windows), o host é "localhost",
# porque foi assim que a porta 1433 foi mapeada no docker-compose.
DATABASE_URL = (
    "mssql+pyodbc://sa:KeyboardProject%40123@localhost,1433/master"
    "?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
)

engine = create_engine(DATABASE_URL, echo=False, future=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    """Classe base de onde todos os models ORM herdam."""
    pass