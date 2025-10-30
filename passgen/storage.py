import hashlib
import os


def hash_password(password: str) -> str:
    """
    Хэширует пароль с использованием SHA-256.

    Args:
        password (str): Пароль для хэширования.

    Returns:
        str: Шестнадцатеричный SHA-256 хэш.
    """
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def save_password(password: str, filename: str) -> None:
    """
    Сохраняет хэш пароля в файл.

    Args:
        password (str): Пароль для сохранения.
        filename (str): Имя файла для записи.

    Raises:
        IOError: Если не удается записать в файл.
    """
    hashed = hash_password(password)
    try:
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(hashed + '\n')
    except IOError as e:
        print(f"Ошибка при записи в файл {filename}: {e}")


def load_passwords(filename: str) -> list:
    """
    Загружает список хэшей паролей из файла.

    Args:
        filename (str): Имя файла для чтения.

    Returns:
        list[str]: Список хэшей паролей.

    Raises:
        IOError: Если не удается прочитать файл.
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Файл {filename} не найден.")
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read().splitlines()
    except IOError as e:
        print(f"Ошибка при чтении файла {filename}: {e}")
        return []
