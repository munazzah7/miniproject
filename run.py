import time
from pynput.keyboard import Key, Listener

last_key = None
last_time = 0
keystroke_message = ""

def on_press(key):
    global keystroke_message, last_key, last_time
    current_time = time.time()
    try:
        if hasattr(key, 'char') and key.char is not None:
            if key.char == last_key and (current_time - last_time) < 0.3:
                return
            keystroke_message += key.char
            last_key = key.char
            last_time = current_time
        else:
            if key == Key.space:
                keystroke_message += ' '
            elif key == Key.enter:
                keystroke_message += '\n'
            elif key == Key.tab:
                keystroke_message += '\t'
            elif key == Key.backspace:
                keystroke_message = keystroke_message[:-1]
            else:
                keystroke_message += f'[{key.name}]'
    except:
        pass

def on_release(key):
    if key == Key.esc:
        return False

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
