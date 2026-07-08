"""
KeyboardProject
----------------
Escuta o teclado e exibe no terminal qual tecla foi pressionada.
Pressione ESC para encerrar o programa.
"""

from pynput import keyboard

count = 0


def start_listening(callback):
    print("Escutando o teclado... (pressione ESC para sair)\n")
    with keyboard.Listener(on_press=callback) as listener:
        listener.join()


def show_key(key):
    """Exibe a tecla pressionada."""
    try:
        print(f"Key: {key} | Key Char: '{key.char}'")
    except AttributeError:
        print(f"Key: {key} | Key Name: {key.name}")

    if key == keyboard.Key.esc:
        print("\nESC pressionado. Encerrando...")
        return False


def show_key_with_counter(key):
    """Exibe a tecla pressionada e conta quantas foram normais vs. especiais."""
    global count
    try:
        print(f"Key: {key} | Key Char: '{key.char}'")
        count += 1
        print(f"Contador: {count}")
    except AttributeError:
        print(f"Key: {key} | Key Name: {key.name}")
        count -= 1
        print(f"Contador: {count}")

    if key == keyboard.Key.esc:
        print("\nESC pressionado. Encerrando...")
        return False