"""Тесты для модуля database.py - работы с базой данных."""

import unittest
from unittest.mock import patch, MagicMock
from passgen.database import PasswordDatabase


class TestPasswordDatabase(unittest.TestCase):
    """Тестирует класс PasswordDatabase."""
    
    def setUp(self):
        """Подготовка тестового окружения."""
        self.db = PasswordDatabase()
    
    @patch('passgen.database.psycopg2.connect')
    def test_create_table(self, mock_connect):
        """Тест создания таблицы."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        
        self.db.create_table()
        
        # Проверяем, что был выполнен SQL запрос
        mock_cursor.execute.assert_called()
        self.assertIn("CREATE TABLE IF NOT EXISTS passwords", mock_cursor.execute.call_args[0][0])
        mock_conn.commit.assert_called_once()
    
    @patch('passgen.database.psycopg2.connect')
    @patch('passgen.database.encrypt_password')
    def test_save_password(self, mock_encrypt, mock_connect):
        """Тест сохранения пароля."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_encrypt.return_value = "encrypted_password"
        
        self.db.save_password("user1", "service1", "plain_password")
        
        # Проверяем шифрование
        mock_encrypt.assert_called_once_with("plain_password")
        
        # Проверяем SQL запрос
        mock_cursor.execute.assert_called_once()
        args = mock_cursor.execute.call_args[0]
        self.assertIn("INSERT INTO passwords", args[0])
        self.assertEqual(args[1], ("user1", "service1", "encrypted_password"))
    
    @patch('passgen.database.psycopg2.connect')
    @patch('passgen.database.decrypt_password')
    def test_get_password(self, mock_decrypt, mock_connect):
        """Тест получения пароля."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        
        # Настраиваем возвращаемое значение
        mock_cursor.fetchone.return_value = ("encrypted_password",)
        mock_decrypt.return_value = "plain_password"
        
        result = self.db.get_password("user1", "service1")
        
        # Проверяем SQL запрос
        mock_cursor.execute.assert_called_once()
        args = mock_cursor.execute.call_args[0]
        self.assertIn("SELECT encrypted_password FROM passwords", args[0])
        self.assertEqual(args[1], ("user1", "service1"))
        
        # Проверяем дешифровку
        mock_decrypt.assert_called_once_with("encrypted_password")
        self.assertEqual(result, "plain_password")
    
    @patch('passgen.database.psycopg2.connect')
    @patch('passgen.database.decrypt_password')
    def test_get_password_not_found(self, mock_decrypt, mock_connect):
        """Тест получения несуществующего пароля."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        
        # Настраиваем возвращаемое значение (нет записей)
        mock_cursor.fetchone.return_value = None
        
        result = self.db.get_password("user1", "service1")
        
        self.assertIsNone(result)
        mock_decrypt.assert_not_called()
    
    @patch('passgen.database.psycopg2.connect')
    @patch('passgen.database.decrypt_password')
    def test_search_by_username(self, mock_decrypt, mock_connect):
        """Тест поиска по имени пользователя."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        
        # Настраиваем возвращаемые значения
        mock_cursor.fetchall.return_value = [
            ("service1", "encrypted1"),
            ("service2", "encrypted2")
        ]
        mock_decrypt.side_effect = ["plain1", "plain2"]
        
        results = self.db.search_by_username("user1")
        
        # Проверяем SQL запрос
        mock_cursor.execute.assert_called_once()
        args = mock_cursor.execute.call_args[0]
        self.assertIn("SELECT service, encrypted_password", args[0])
        self.assertEqual(args[1], ("user1",))
        
        # Проверяем результаты
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0], ("service1", "plain1"))
        self.assertEqual(results[1], ("service2", "plain2"))
    
    @patch('passgen.database.psycopg2.connect')
    @patch('passgen.database.decrypt_password')
    def test_search_by_username_decrypt_error(self, mock_decrypt, mock_connect):
        """Тест обработки ошибки дешифровки при поиске по имени."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        
        mock_cursor.fetchall.return_value = [("service1", "encrypted1")]
        mock_decrypt.side_effect = ValueError("Decryption error")
        
        results = self.db.search_by_username("user1")
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], ("service1", "[Ошибка расшифровки]"))
    
    @patch('passgen.database.psycopg2.connect')
    @patch('passgen.database.decrypt_password')
    def test_get_all_records(self, mock_decrypt, mock_connect):
        """Тест получения всех записей."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        
        # Настраиваем возвращаемые значения
        mock_cursor.fetchall.return_value = [
            ("user1", "service1", "encrypted1", "2024-01-01 12:00:00"),
            ("user2", "service2", "encrypted2", "2024-01-02 13:00:00")
        ]
        mock_decrypt.side_effect = ["plain1", "plain2"]
        
        results = self.db.get_all_records()
        
        # Проверяем SQL запрос
        mock_cursor.execute.assert_called_once()
        
        # Проверяем результаты
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['username'], "user1")
        self.assertEqual(results[0]['service'], "service1")
        self.assertEqual(results[0]['password'], "plain1")
        self.assertEqual(results[0]['created_at'], "2024-01-01 12:00:00")
        
        self.assertEqual(results[1]['username'], "user2")
        self.assertEqual(results[1]['service'], "service2")
        self.assertEqual(results[1]['password'], "plain2")
        self.assertEqual(results[1]['created_at'], "2024-01-02 13:00:00")


if __name__ == '__main__':
    unittest.main()