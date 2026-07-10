from Config.database import init_db
from Service.keyboard_listener import start_listening, show_key

if __name__ == "__main__":
    init_db()  # cria a tabela KeyHistory se ainda não existir
    start_listening(show_key)