"""Тесты для модуля generator.py - генерации безопасных паролей."""

import unittest
import string
from passgen.generator import generate_password


class TestPasswordGenerator(unittest.TestCase):
    """Тестирует функцию generate_password из модуля generator."""
    
    def test_default_length(self):
        """Тест генерации пароля со значениями по умолчанию.
        
        Проверяет, что пароль имеет длину 12 символов при вызове без параметров.
        """
        password = generate_password()
        self.assertEqual(len(password), 12)
    
    def test_custom_length(self):
        """Тест генерации пароля заданной длины.
        
        Проверяет корректность работы параметра length.
        """
        password = generate_password(length=15)
        self.assertEqual(len(password), 15)
    
    def test_contains_selected_chars(self):
        """Тест наличия выбранных типов символов в пароле.
        
        Проверяет, что пароль содержит заглавные буквы, цифры и спецсимволы
        при включенных соответствующих опциях.
        """
        password = generate_password(use_uppercase=True, use_digits=True, use_special=True, length=24)
        self.assertTrue(any(c in string.ascii_uppercase for c in password)) 
        self.assertTrue(any(c in string.digits for c in password))
        self.assertTrue(any(c in string.punctuation for c in password))
    
    def test_only_lowercase_when_all_disabled(self):
        """Тест генерации только строчных букв при отключенных опциях.
        
        Проверяет, что при отключении всех опций пароль состоит только из строчных букв.
        """
        password = generate_password(use_uppercase=False, use_digits=False, use_special=False)
        self.assertTrue(all(c in string.ascii_lowercase for c in password))
        self.assertEqual(len(password), 12)


if __name__ == '__main__':
    unittest.main()