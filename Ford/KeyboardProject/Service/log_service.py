"""
HistoryRepository
------------------
Responsável por persistir e ler registros de KeyHistory:
- Em um arquivo local no formato JSON Lines (.jsonl)
- E agora também no banco de dados (SQL Server), via SQLAlchemy
 
Por que manter os dois?
- O .jsonl é rápido, não depende do banco estar de pé, e serve como
  um "log local" independente.
- O banco permite consultas mais robustas, relatórios, integração
  com outras ferramentas, etc — mais alinhado com o que se espera
  de um projeto "de verdade".
"""
 
import json
from datetime import datetime
from pathlib import Path
 
from Model.key_history import KeyHistory
from Model.orm.key_history_orm import KeyHistoryORM
from config.database import SessionLocal
from config.logconfig.logger_config import setup_logger
 
logger = setup_logger()
 
DEFAULT_FILE_PATH = Path("data") / "key_history.jsonl"
 
 
def save(entry: KeyHistory, file_path: Path = DEFAULT_FILE_PATH) -> None:
    """
    Adiciona um registro de KeyHistory no arquivo .jsonl E no banco.
    Depois de salvar no banco, o `entry.id` é preenchido com o
    serial gerado pelo SQL Server.
    """
    # 1. Salva no banco primeiro, para conseguir capturar o id gerado
    _save_to_database(entry)
 
    # 2. Salva no arquivo local, já com o id preenchido
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, mode="a", encoding="utf-8") as f:
        linha = json.dumps(entry.to_dict(), ensure_ascii=False)
        f.write(linha + "\n")
 
 
def _save_to_database(entry: KeyHistory) -> None:
    """Insere o registro no banco e preenche entry.id com o serial gerado."""
    session = SessionLocal()
    try:
        registro_orm = KeyHistoryORM(
            key=entry.key,
            press_time=entry.press_time,
            ip_address=entry.ip_address,
        )
        session.add(registro_orm)
        session.flush()  # gera o id (IDENTITY) sem precisar commitar ainda
        entry.id = registro_orm.id
        session.commit()
        logger.debug(f"Registro salvo no banco com id={entry.id}")
    except Exception:
        session.rollback()
        logger.exception("Falha ao salvar o registro no banco de dados")
        raise
    finally:
        session.close()
 
 
def load_all(file_path: Path = DEFAULT_FILE_PATH) -> list[dict]:
    """Lê todos os registros salvos no arquivo local e retorna como lista de dicionários."""
    if not file_path.exists():
        return []
 
    registros = []
    with open(file_path, mode="r", encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if linha:
                registros.append(json.loads(linha))
    return registros
 
 
def rebuild_text(
    start: datetime,
    end: datetime,
    file_path: Path = DEFAULT_FILE_PATH,
) -> str:
    """
    Reconstrói o texto digitado entre `start` e `end`, na ordem
    cronológica em que as teclas foram pressionadas.
 
    Regras:
    - 'space'      -> adiciona um espaço
    - 'backspace'  -> remove o último caractere já montado
    - nome de tecla com mais de 1 caractere (ex: 'shift', 'ctrl',
      'enter', 'esc'...) -> ignora, não é um caractere "digitável"
    - qualquer outra tecla (letras, números, símbolos) -> adiciona
      o caractere direto
    """
    registros = load_all(file_path)
 
    registros_no_periodo = []
    for registro in registros:
        press_time = datetime.fromisoformat(registro["press_time"])
        if start <= press_time <= end:
            registros_no_periodo.append((press_time, registro["key"]))
 
    registros_no_periodo.sort(key=lambda item: item[0])
 
    caracteres = []
    for _, key in registros_no_periodo:
        if key == "space":
            caracteres.append(" ")
        elif key == "backspace":
            if caracteres:
                caracteres.pop()
        elif len(key) > 1:
            continue
        else:
            caracteres.append(key)
 
    return "".join(caracteres)