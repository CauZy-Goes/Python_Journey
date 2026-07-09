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


# Exemplo de uso
if __name__ == "__main__":
    from datetime import datetime

    exemplo = KeyHistory(key="a", press_time=datetime.now())
    save(exemplo)

    print("Registros salvos até agora:")
    for registro in load_all():
        print(registro)