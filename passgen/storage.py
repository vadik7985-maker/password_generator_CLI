"""Модуль для безопасного шифрования паролей."""

from cryptography.fernet import Fernet
import base64
import os

# Генерируем или загружаем ключ шифрования
KEY_FILE = "passgen_key.key"


def get_encryption_key() -> bytes:
    """Получает ключ шифрования из файла или генерирует новый."""
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'rb') as f:
            return f.read()
    else:
        # Генерируем новый ключ
        key = Fernet.generate_key()
        with open(KEY_FILE, 'wb') as f:
            f.write(key)
        print(f"Создан новый ключ шифрования: {KEY_FILE}")
        return key


def encrypt_password(password: str) -> str:
    """Шифрует пароль для хранения в БД.
    
    Args:
        password (str): Пароль в открытом виде
        
    Returns:
        str: Зашифрованный пароль в base64
    """
    key = get_encryption_key()
    fernet = Fernet(key)
    
    # Шифруем пароль и кодируем в base64 для хранения в текстовом поле БД
    encrypted = fernet.encrypt(password.encode())
    return base64.b64encode(encrypted).decode('utf-8')


def decrypt_password(encrypted_password: str) -> str:
    """Расшифровывает пароль из БД.
    
    Args:
        encrypted_password (str): Зашифрованный пароль в base64
        
    Returns:
        str: Пароль в открытом виде
        
    Raises:
        ValueError: Если не удалось расшифровать
    """
    try:
        key = get_encryption_key()
        fernet = Fernet(key)
        
        # Декодируем из base64 и расшифровываем
        encrypted_bytes = base64.b64decode(encrypted_password)
        decrypted = fernet.decrypt(encrypted_bytes)
        
        return decrypted.decode('utf-8')
    except Exception as e:
        raise ValueError(f"Ошибка расшифровки: {e}")