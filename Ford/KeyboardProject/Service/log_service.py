"""
HistoryRepository
------------------
Responsável por persistir e ler registros de KeyHistory em um
arquivo no formato JSON Lines (.jsonl) — um objeto JSON por linha.

Por que JSON Lines e não um único array JSON?
- Permite usar "append" (adicionar no final do arquivo) sem precisar
  reabrir e reescrever o arquivo inteiro a cada tecla pressionada.
- Se o programa travar no meio, as linhas já escritas continuam válidas
  (um array JSON incompleto quebraria o arquivo inteiro).
"""

import json
from pathlib import Path

from datetime import datetime

from Model.key_history import KeyHistory

DEFAULT_FILE_PATH = Path("data") / "key_history.jsonl"


def save(entry: KeyHistory, file_path: Path = DEFAULT_FILE_PATH) -> None:
    """Adiciona um registro de KeyHistory no final do arquivo .jsonl."""
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, mode="a", encoding="utf-8") as f:
        linha = json.dumps(entry.to_dict(), ensure_ascii=False)
        f.write(linha + "\n")

def load_all(file_path: Path = DEFAULT_FILE_PATH) -> list[dict]:
    """Lê todos os registros salvos e retorna como lista de dicionários."""
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
 
    # Filtra pelo período e converte press_time de volta para datetime
    registros_no_periodo = []
    for registro in registros:
        press_time = datetime.fromisoformat(registro["press_time"])
        if start <= press_time <= end:
            registros_no_periodo.append((press_time, registro["key"]))
 
    # Ordena em ordem crescente de tempo (garantia extra, caso o
    # arquivo não esteja 100% em ordem)
    registros_no_periodo.sort(key=lambda item: item[0])
 
    caracteres = []
    for _, key in registros_no_periodo:
        if key == "space":
            caracteres.append(" ")
        elif key == "backspace":
            if caracteres:
                caracteres.pop()
        elif len(key) > 1:
            # Tecla especial (shift, ctrl, enter, esc, etc.) -> ignora
            continue
        else:
            caracteres.append(key)
 
    return "".join(caracteres)