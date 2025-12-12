"""Тесты для модуля storage.py - шифрования и дешифрования паролей."""

import unittest
import os
import tempfile
from unittest.mock import patch, mock_open
from cryptography.fernet import Fernet
import base64
from passgen.storage import get_encryption_key, encrypt_password, decrypt_password


class TestStorage(unittest.TestCase):
    """Тестирует функции работы с шифрованием паролей."""
    
    def setUp(self):
        """Подготовка тестового окружения.
        
        Создает временный ключевой файл для каждого теста.
        """
        self.temp_key_file = tempfile.mktemp()
    
    def tearDown(self):
        """Очистка после тестов.
        
        Удаляет временные файлы если они существуют.
        """
        if os.path.exists(self.temp_key_file):
            os.remove(self.temp_key_file)
    
    @patch('passgen.storage.KEY_FILE', 'test_key.key')
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_get_existing_key(self, mock_file, mock_exists):
        """Тест получения существующего ключа из файла."""
        mock_exists.return_value = True
        test_key = Fernet.generate_key()
        mock_file.return_value.read.return_value = test_key
        
        key = get_encryption_key()
        self.assertEqual(key, test_key)
    
    @patch('passgen.storage.KEY_FILE', 'test_key.key')
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_generate_new_key(self, mock_file, mock_exists):
        """Тест генерации нового ключа при отсутствии файла."""
        mock_exists.return_value = False
        
        key = get_encryption_key()
        
        # Проверяем, что файл был открыт для записи
        mock_file.assert_called_with('test_key.key', 'wb')
        
        # Проверяем, что был вызван Fernet.generate_key()
        # (не можем проверить непосредственно, но можем проверить что ключ валиден)
        self.assertIsInstance(key, bytes)
        self.assertEqual(len(key), 44)  # Длина Fernet ключа в base64
    
    def test_encrypt_decrypt_roundtrip(self):
        """Тест полного цикла шифрования и дешифрования.
        
        Проверяет, что зашифрованный и расшифрованный пароль совпадает с исходным.
        """
        # Создаем временный ключ для теста
        test_key = Fernet.generate_key()
        
        with patch('passgen.storage.get_encryption_key', return_value=test_key):
            original_password = "MySuperSecretPassword123!@#"
            
            # Шифруем пароль
            encrypted = encrypt_password(original_password)
            
            # Проверяем, что результат - валидный base64
            self.assertIsInstance(encrypted, str)
            try:
                base64.b64decode(encrypted)
            except Exception:
                self.fail("encrypt_password не вернула валидный base64")
            
            # Расшифровываем обратно
            decrypted = decrypt_password(encrypted)
            
            # Проверяем совпадение
            self.assertEqual(decrypted, original_password)
    
    def test_encrypt_different_passwords(self):
        """Тест шифрования разных паролей.
        
        Проверяет, что разные пароли дают разные зашифрованные результаты.
        """
        test_key = Fernet.generate_key()
        
        with patch('passgen.storage.get_encryption_key', return_value=test_key):
            password1 = "password1"
            password2 = "password2"
            
            encrypted1 = encrypt_password(password1)
            encrypted2 = encrypt_password(password2)
            
            self.assertNotEqual(encrypted1, encrypted2)
    
    def test_decrypt_invalid_base64(self):
        """Тест дешифрования невалидного base64.
        
        Проверяет, что функция выбрасывает ValueError при невалидных данных.
        """
        test_key = Fernet.generate_key()
        
        with patch('passgen.storage.get_encryption_key', return_value=test_key):
            with self.assertRaises(ValueError):
                decrypt_password("невалидный-base64")
    
    def test_decrypt_with_wrong_key(self):
        """Тест дешифрования с неправильным ключом.
        
        Проверяет, что попытка расшифровать с другим ключом вызывает ошибку.
        """
        # Шифруем с одним ключом
        key1 = Fernet.generate_key()
        with patch('passgen.storage.get_encryption_key', return_value=key1):
            encrypted = encrypt_password("test")
        
        # Пытаемся расшифровать с другим ключом
        key2 = Fernet.generate_key()
        with patch('passgen.storage.get_encryption_key', return_value=key2):
            with self.assertRaises(ValueError):
                decrypt_password(encrypted)
    
    def test_encrypt_empty_password(self):
        """Тест шифрования пустого пароля."""
        test_key = Fernet.generate_key()
        
        with patch('passgen.storage.get_encryption_key', return_value=test_key):
            encrypted = encrypt_password("")
            decrypted = decrypt_password(encrypted)
            self.assertEqual(decrypted, "")
    
    def test_encrypt_special_characters(self):
        """Тест шифрования паролей со специальными символами."""
        test_key = Fernet.generate_key()
        
        test_passwords = [
            "пароль с пробелами",
            "unicode✓✓✓",
            "emoji",
            "new\nline",
            "tab\tcharacter",
            "null\0byte",
        ]
        
        with patch('passgen.storage.get_encryption_key', return_value=test_key):
            for password in test_passwords:
                with self.subTest(password=password):
                    encrypted = encrypt_password(password)
                    decrypted = decrypt_password(encrypted)
                    self.assertEqual(decrypted, password)


if __name__ == '__main__':
    unittest.main()