"""
KeyboardProject
----------------
Escuta o teclado e exibe no terminal qual tecla foi pressionada.
Pressione ESC para encerrar o programa.
"""

from pynput import keyboard

count = 0


def start_listening(callback):
    print("Listening keyboard... (press ESC to exit)\n")
    with keyboard.Listener(on_press=callback) as listener:
        listener.join()


def show_key(key):
    """Show the pressed key."""
    try:
        print(f"Key: {key} | Key Char: '{key.char}'")
    except AttributeError:
        print(f"Key: {key} | Key Name: {key.name}")

    if key == keyboard.Key.esc:
        print("\nESC pressed. Ending...")
        return False

count: float = 0.0


def counter(key):
    global count
    try:
        if key == keyboard.Key.esc:
            print("\nESC pressed. Ending...")
            return False

        if key == keyboard.Key.up:
            print(f"'{count}' + 1")
            count += 1
            print(count)
        
        if key == keyboard.Key.down:
            print(f"'{count}' - 1")
            count -= 1
            print(count)

        if key == keyboard.Key.right:
            print(f"'{count}' * 10")
            count *= 10
            print(count)

        if key == keyboard.Key.left:
            print(f"'{count}' / 10")
            count /= 10
            print(count)

        if key == keyboard.Key.enter:
           count = 0.0
           print(f"count reset")
        
    except AttributeError:
        pass