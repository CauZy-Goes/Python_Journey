"""
KeyboardProject
----------------
Escuta o teclado e exibe no terminal qual tecla foi pressionada.
Pressione ESC para encerrar o programa.
"""

from pynput import keyboard



def start_listening():
    print("Escutando o teclado... (pressione ESC para sair)\n")
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

def on_press(key):
    try:
        # Teclas "normais" (letras, números, símbolos)
        print(f"Key: {key} | Key Char: '{key.char}' | Key Name: {key.name}")
    except AttributeError:
        # Teclas especiais (Shift, Ctrl, Enter, setas, etc.)
        print(f"Key: {key} | Key Name: {key.name}")

    # Encerra o listener se a tecla ESC for pressionada
    if key == keyboard.Key.esc:
        print("\nESC pressionado. Encerrando...")
        return False
