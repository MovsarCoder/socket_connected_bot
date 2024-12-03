import random
import string


def generate_password(length=10) -> str:
    # Для генерации пароля состоящего из букв
    all_chars = string.digits

    # Для генерации пароля состоящего из букв и символов
    # all_chars = string.ascii_letters + string.digits + string.punctuation

    password = ''.join(random.choice(all_chars) for _ in range(length))
    return password
