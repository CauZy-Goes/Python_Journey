from Service.keyboard_listener import start_listening, show_key
from Model.key_history import KeyHistory

if __name__ == "__main__":
    start_listening(show_key)   # troca aqui pra escolher o comportamento

# if __name__ == "__main__":
#     start_listening(counter)   # troca aqui pra escolher o comportamento

# # Exemplo de uso
# if __name__ == "__main__":
#     registro = KeyHistory(key="a")
#     print(registro)