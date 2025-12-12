"""Тесты для модуля utils.py - валидации параметров генерации пароля."""

import unittest
from unittest.mock import patch
from io import StringIO
from passgen.utils import validate_args


class TestUtils(unittest.TestCase):
    """Тестирует функцию validate_args из модуля utils."""
    
    def test_validate_args_positive_length(self):
        """Тест валидации корректной длины.
        
        Проверяет, что функция не вызывает исключений при корректных данных.
        """
        # Не должно вызывать исключений
        validate_args(10, True, True, True)
        validate_args(1, False, False, False)
    
    def test_validate_args_zero_length(self):
        """Тест ошибки при длине 0.
        
        Проверяет, что функция выбрасывает ValueError при длине 0.
        """
        with self.assertRaises(ValueError) as context:
            validate_args(0, True, True, True)
        self.assertIn("Длина пароля должна быть положительным числом", str(context.exception))
    
    def test_validate_args_negative_length(self):
        """Тест ошибки при отрицательной длине.
        
        Проверяет, что функция выбрасывает ValueError при отрицательной длине.
        """
        with self.assertRaises(ValueError) as context:
            validate_args(-5, True, True, True)
        self.assertIn("Длина пароля должна быть положительным числом", str(context.exception))
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_warning_when_no_char_types(self, mock_stdout):
        """Тест предупреждения при отсутствии типов символов.
        
        Проверяет, что выводится предупреждение когда не выбраны
        спецсимволы, цифры или заглавные буквы.
        """
        validate_args(10, False, False, False)
        output = mock_stdout.getvalue()
        self.assertIn("Предупреждение", output)
        self.assertIn("строчные буквы", output)
    
    def test_no_warning_when_char_types_present(self):
        """Тест отсутствия предупреждения при наличии типов символов.
        
        Проверяет, что предупреждение не выводится когда выбраны
        хотя бы один тип символов.
        """
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            validate_args(10, True, True, True)
            output = mock_stdout.getvalue()
            self.assertEqual("", output)
    
    def test_boundary_length_1(self):
        """Тест граничного случая - длина 1.
        
        Проверяет, что функция принимает минимальную допустимую длину 1.
        """
        # Не должно вызывать исключений
        validate_args(1, True, True, True)
    
    def test_various_combinations(self):
        """Тест различных комбинаций параметров."""
        test_cases = [
            (8, True, False, False),
            (16, False, True, False),
            (20, False, False, True),
            (12, True, True, False),
            (14, False, True, True),
            (18, True, False, True),
        ]
        
        for length, special, digits, uppercase in test_cases:
            with self.subTest(length=length, special=special, digits=digits, uppercase=uppercase):
                try:
                    validate_args(length, special, digits, uppercase)
                except Exception as e:
                    self.fail(f"validate_args вызвала исключение {e} для параметров: "
                             f"length={length}, special={special}, digits={digits}, uppercase={uppercase}")


if __name__ == '__main__':
    unittest.main()