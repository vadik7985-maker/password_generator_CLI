"""Тесты для модуля storage.py - хранения и загрузки хэшированных паролей."""

import unittest
import os
import tempfile
from passgen.storage import hash_password, save_password, load_passwords


class TestStorage(unittest.TestCase):
    """Тестирует функции работы с хранилищем паролей."""
    
    def setUp(self):
        """Подготовка тестового окружения.
        
        Создает временный файл для каждого теста.
        """
        self.temp_file = tempfile.mktemp()
    
    def test_hash_consistency(self):
        """Тест консистентности хэширования.
        
        Проверяет, что один и тот же пароль всегда дает одинаковый хэш.
        """
        hash1 = hash_password("test123")
        hash2 = hash_password("test123")
        self.assertEqual(hash1, hash2)
    
    def test_save_and_load(self):
        """Тест сохранения и загрузки пароля.
        
        Проверяет полный цикл: сохранение пароля в файл и его последующую загрузку.
        """
        save_password("mypassword", self.temp_file)
        hashes = load_passwords(self.temp_file)
        self.assertEqual(len(hashes), 1)
        self.assertEqual(hashes[0], hash_password("mypassword"))
    
    def test_save_multiple(self):
        """Тест сохранения нескольких паролей.
        
        Проверяет, что функция save_password добавляет пароли в конец файла,
        а не перезаписывает его.
        """
        save_password("pass1", self.temp_file)
        save_password("pass2", self.temp_file)
        hashes = load_passwords(self.temp_file)
        self.assertEqual(len(hashes), 2)
    
    def test_load_nonexistent_file(self):
        """Тест загрузки из несуществующего файла.
        
        Проверяет, что функция load_passwords корректно обрабатывает
        случай отсутствия файла.
        """
        with self.assertRaises(FileNotFoundError):
            load_passwords("nonexistent.txt")


if __name__ == '__main__':
    unittest.main()