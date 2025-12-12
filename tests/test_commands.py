"""Тесты для модуля commands.py - обработки команд CLI."""

import unittest
from unittest.mock import patch, MagicMock, mock_open
from io import StringIO
import sys
sys.path.append('.')
from passgen.commands import handle_commands


class TestCommands(unittest.TestCase):
    """Тестирует функцию handle_commands - основную логику CLI."""
    
    def mock_args(self, **kwargs):
        """Создает mock-объект аргументов командной строки."""
        args = MagicMock()
        # Устанавливаем значения по умолчанию для всех необходимых атрибутов
        default_args = {
            'save': None,
            'find_by_username': None,
            'find_by_service': None,
            'find_by_both': None,
            'show_all': False,
            'generate': False,
            'length': 12,
            'special': True,
            'digits': True,
            'uppercase': True
        }
        default_args.update(kwargs)  # Обновляем переданными значениями
        for key, value in default_args.items():
            setattr(args, key, value)
        return args
    
    @patch('passgen.commands.PasswordDatabase')
    def test_generate_password(self, mock_db_class):
        """Тест команды генерации пароля.
        
        Проверяет, что при вызове происходит генерация пароля
        и вывод результата в консоль.
        """
        mock_db = MagicMock()
        mock_db_class.return_value = mock_db
        
        args = self.mock_args(generate=True)
        
        # Перехватываем вывод и ввод
        with patch('passgen.commands.generate_password') as mock_generate, \
             patch('sys.stdout', new_callable=StringIO) as mock_stdout, \
             patch('builtins.input', return_value='n'):
            
            mock_generate.return_value = "Abc123!@#"
            handle_commands(args)
            output = mock_stdout.getvalue()
        
        # Проверяем вывод
        self.assertIn("Сгенерирован пароль:", output)
        self.assertIn("Abc123!@#", output)
    
    @patch('passgen.commands.PasswordDatabase')
    def test_save_password_command(self, mock_db_class):
        """Тест команды сохранения пароля."""
        mock_db = MagicMock()
        mock_db_class.return_value = mock_db
        
        args = self.mock_args(save="user:service:mypassword")
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            handle_commands(args)
            output = mock_stdout.getvalue()
        
        # Проверяем, что вызван метод сохранения
        mock_db.save_password.assert_called_once_with("user", "service", "mypassword")
        self.assertIn("Пароль сохранен!", output)
    
    @patch('passgen.commands.PasswordDatabase')
    def test_save_password_invalid_format(self, mock_db_class):
        """Тест сохранения пароля с неверным форматом."""
        mock_db = MagicMock()
        mock_db_class.return_value = mock_db
        
        args = self.mock_args(save="user:service")  
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            handle_commands(args)
            output = mock_stdout.getvalue()
        
        self.assertIn("Ошибка: неверный формат", output)
        mock_db.save_password.assert_not_called()
    
    @patch('passgen.commands.PasswordDatabase')
    def test_find_by_username(self, mock_db_class):
        """Тест поиска по имени пользователя."""
        mock_db = MagicMock()
        mock_db_class.return_value = mock_db
        mock_db.search_by_username.return_value = [
            ("service1", "pass1"),
            ("service2", "pass2")
        ]
        
        args = self.mock_args(find_by_username="user1")
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            handle_commands(args)
            output = mock_stdout.getvalue()
        
        mock_db.search_by_username.assert_called_once_with("user1")
        self.assertIn("Найдено паролей для пользователя 'user1'", output)
        self.assertIn("service1", output)
        self.assertIn("service2", output)
    
    @patch('passgen.commands.PasswordDatabase')
    def test_find_by_service(self, mock_db_class):
        """Тест поиска по сервису."""
        mock_db = MagicMock()
        mock_db_class.return_value = mock_db
        mock_db.search_by_service.return_value = [
            ("user1", "pass1"),
            ("user2", "pass2")
        ]
        
        args = self.mock_args(find_by_service="gmail")
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            handle_commands(args)
            output = mock_stdout.getvalue()
        
        mock_db.search_by_service.assert_called_once_with("gmail")
        self.assertIn("Найдено паролей для сервиса 'gmail'", output)
        self.assertIn("user1", output)
        self.assertIn("user2", output)
    
    @patch('passgen.commands.PasswordDatabase')
    def test_show_all_records(self, mock_db_class):
        """Тест показа всех записей."""
        mock_db = MagicMock()
        mock_db_class.return_value = mock_db
        mock_db.get_all_records.return_value = [
            {
                'username': 'user1',
                'service': 'service1',
                'password': 'pass1',
                'created_at': '2024-01-01 12:00:00'
            }
        ]
        
        args = self.mock_args(show_all=True)
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            handle_commands(args)
            output = mock_stdout.getvalue()
        
        mock_db.get_all_records.assert_called_once()
        self.assertIn("Всего записей в базе", output)
        self.assertIn("user1", output)
        self.assertIn("service1", output)
    
    @patch('passgen.commands.PasswordDatabase')
    def test_db_connection_error(self, mock_db_class):
        """Тест ошибки подключения к БД."""
        mock_db_class.side_effect = Exception("Connection failed")
        
        args = self.mock_args(show_all=True)
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            handle_commands(args)
            output = mock_stdout.getvalue()
        
        self.assertIn("Ошибка подключения к БД", output)


if __name__ == '__main__':
    unittest.main()