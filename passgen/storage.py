"""Модуль для хранения и загрузки хэшированных паролей.

Использует SHA-256 для хэширования и работает с текстовыми файлами.
"""

import hashlib
import os


def hash_password(password: str) -> str:
    """Хэширует пароль с использованием SHA-256.

    Args:
        password (str): Исходный пароль.

    Returns:
        str: Шестнадцатеричная строка хэша SHA-256.

    Raises:
        None
    """
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def save_password(password: str, filename: str) -> None:
    """Сохраняет хэш пароля в файл (добавляет в конец).

    Args:
        password (str): Пароль для сохранения.
        filename (str): Путь к файлу для записи.

    Returns:
        None

    Raises:
        IOError: Если произошла ошибка при записи в файл.
    """
    hashed = hash_password(password)
    try:
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(hashed + '\n')
    except IOError as e:
        print(f"Ошибка при записи в файл {filename}: {e}")


def load_passwords(filename: str) -> list[str]:
    """Загружает список хэшей паролей из файла.

    Args:
        filename (str): Путь к файлу с хэшами.

    Returns:
        list[str]: Список хэшей паролей (строк).

    Raises:
        FileNotFoundError: Если файл не существует.
        IOError: Если произошла ошибка при чтении файла.
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Файл {filename} не найден.")
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read().splitlines()
    except IOError as e:
        print(f"Ошибка при чтении файла {filename}: {e}")
        return []
