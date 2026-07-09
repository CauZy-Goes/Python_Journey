"""
KeyboardProject
----------------
Escuta o teclado e exibe no terminal qual tecla foi pressionada.
Pressione ESC para encerrar o programa.
"""

from datetime import datetime
 
from pynput import keyboard
 
from Model.key_history import KeyHistory
from Service.log_service import save
from Config.Log.log_config import setup_logger

logger = setup_logger()


def start_listening(callback):
    logger.info("Listener Starting...")
    print("Listening keyboard... (press ESC to exit)\n")
    with keyboard.Listener(on_press=callback) as listener:
        listener.join()
    logger.info("Listener Ending...")


def show_key(key):
    """Show the pressed key."""
    try:
        print(f"Key: {key} | Key Char: '{key.char}'")
    except AttributeError:
        print(f"Key: {key} | Key Name: {key.name}")

    if key == keyboard.Key.esc:
        print("\nESC pressed. Ending...")
        return False



# count: float = 0.0


# def counter(key):
#     global count
#     try:
#         if key == keyboard.Key.esc:
#             print("\nESC pressed. Ending...")
#             return False

#         if key == keyboard.Key.up:
#             print(f"'{count}' + 1")
#             count += 1
#             print(count)
        
#         if key == keyboard.Key.down:
#             print(f"'{count}' - 1")
#             count -= 1
#             print(count)

#         if key == keyboard.Key.right:
#             print(f"'{count}' * 10")
#             count *= 10
#             print(count)

#         if key == keyboard.Key.left:
#             print(f"'{count}' / 10")
#             count /= 10
#             print(count)

#         if key == keyboard.Key.enter:
#            count = 0.0
#            print(f"count reset")
        
#     except AttributeError:
#         pass