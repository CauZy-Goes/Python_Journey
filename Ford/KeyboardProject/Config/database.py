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
#
# Usando pymssql em vez de pyodbc: o pymssql já vem com o driver TDS
# (FreeTDS) embutido no próprio pacote pip, então não precisa instalar
# nenhum driver ODBC separado no Windows.
DATABASE_URL = "mssql+pymssql://sa:KeyboardProject%40123@localhost:1433/master"

engine = create_engine(DATABASE_URL, echo=False, future=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    """Classe base de onde todos os models ORM herdam."""
    pass


def init_db() -> None:
    """
    Cria todas as tabelas mapeadas pelos models ORM, caso ainda não existam.

    Precisa que os models já estejam importados antes de chamar essa
    função, para que fiquem registrados em Base.metadata (por isso o
    import de KeyHistoryORM aqui dentro).
    """
    from Model.Orm.key_history_orm import KeyHistoryORM  # noqa: F401

    Base.metadata.create_all(engine)