"""Тесты для модуля commands.py - обработки команд CLI."""

import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
from passgen.commands import handle_commands


class TestCommands(unittest.TestCase):
    """Тестирует функцию handle_commands - основную логику CLI."""
    
    def mock_args(self, **kwargs):
        """Создает mock-объект аргументов командной строки."""
        args = MagicMock()
        # Устанавливаем значения по умолчанию для всех необходимых атрибутов
        default_args = {
            'find': None,
            'find_file': None,
            'length': 12,
            'special': True,
            'digits': True,
            'uppercase': True,
            'output': None
        }
        default_args.update(kwargs)  # Обновляем переданными значениями
        for key, value in default_args.items():
            setattr(args, key, value)
        return args
    
    @patch('passgen.commands.generate_password')  # заменяем реальный объеки на "муляж"
    def test_generate_password(self, mock_generate):
        """Тест команды генерации пароля.
        
        Проверяет, что при вызове происходит генерация пароля
        и вывод результата в консоль.
        """
        mock_generate.return_value = "Abc123!@#" # Настраиваем муляж генератора чтобы он всегда возвращал "Abc123!@#"
        args = self.mock_args()  # Используем значения по умолчанию
        
        # "Перехватываем" всё что программа печатает в консоль
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            handle_commands(args)
            output = mock_stdout.getvalue() # Получаем всё что было напечатано
        
        self.assertIn("Сгенерированный пароль: Abc123!@#", output)
    
    @patch('passgen.commands.generate_password')
    @patch('passgen.commands.save_password')
    def test_generate_and_save(self, mock_save, mock_generate):
        """Тест генерации пароля с сохранением в файл.
        
        Проверяет, что при указании флага -o/--output пароль сохраняется в файл.
        """
        mock_generate.return_value = "TestPass123"
        args = self.mock_args(output="passwords.txt")   # Создаем аргументы с указанием файла для сохранения
        
        # Перехватить вывод программы
        with patch('sys.stdout', new_callable=StringIO):
            handle_commands(args)
        
         # Проверяем, что функция save_password была вызвана ровно один раз
        mock_save.assert_called_once_with("TestPass123", "passwords.txt")
    
    def test_find_password(self):
        """Тест команды поиска пароля.
        
        Проверяет корректность работы флагов --find и --find-file
        при поиске хэшированного пароля в файле.
        """
        # Создаем аргументы для поиска пароля
        args = self.mock_args(find="mypassword", find_file="passwords.txt")
        
        # Подменяем три функции одновременно используя контекстный менеджер
        with patch('passgen.commands.hash_password') as mock_hash, \
             patch('passgen.commands.load_passwords') as mock_load, \
             patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            
            # Настраиваем муляж хэширования - всегда возвращает фиксированный хэш
            mock_hash.return_value = "abc123"
            mock_load.return_value = ["xyz789", "abc123", "def456"]
            
            handle_commands(args)
            output = mock_stdout.getvalue()
        
        self.assertIn("Пароль найден в файле", output)


if __name__ == '__main__':
    unittest.main()