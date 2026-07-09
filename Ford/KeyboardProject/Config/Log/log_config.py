"""
logger_config
-------------
Configuração central do log técnico da aplicação (não confundir com o
histórico de teclas — isso aqui é sobre o comportamento do PROGRAMA:
erros, avisos, eventos de início/fim, etc).
"""

import logging
from pathlib import Path

LOG_FILE = Path("logs") / "app.log"


def setup_logger(name: str = "keyboard_project") -> logging.Logger:
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Evita duplicar handlers se setup_logger for chamado mais de uma vez
    if logger.handlers:
        return logger

    formato = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%d/%m/%Y %H:%M:%S",
    )

    # Handler de arquivo: guarda tudo, inclusive DEBUG
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formato)

    # Handler de console: só mostra INFO pra cima (menos poluído)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formato)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# Exemplo de uso
if __name__ == "__main__":
    logger = setup_logger()
    logger.debug("Mensagem de debug — só aparece no arquivo")
    logger.info("Listener iniciado")
    logger.warning("Algo merece atenção, mas não é um erro")
    logger.error("Algo deu errado ao salvar o arquivo")