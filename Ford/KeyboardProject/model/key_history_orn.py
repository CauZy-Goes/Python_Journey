"""
KeyHistoryORM
-------------
Representação da tabela `KeyHistory` no banco de dados, usada pelo
SQLAlchemy para mapear objetos Python <-> linhas da tabela.

Esse é o model "de banco" — diferente do Model/key_history.py, que é
o dataclass usado na aplicação (memória, JSON Lines, etc). Manter os
dois separados evita acoplar a lógica da aplicação diretamente ao
ORM (se um dia trocar de SQL Server para outro banco, ou remover o
ORM, o dataclass da aplicação não precisa mudar).
"""

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from config.database import Base


class KeyHistoryORM(Base):
    __tablename__ = "KeyHistory"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    key: Mapped[str] = mapped_column(String(50), nullable=False)
    press_time: Mapped["DateTime"] = mapped_column(DateTime, nullable=False)
    ip_address: Mapped[str] = mapped_column(String(45), nullable=False)

    def __repr__(self):
        return (
            f"KeyHistoryORM(id={self.id}, key='{self.key}', "
            f"press_time={self.press_time}, ip_address='{self.ip_address}')"
        )