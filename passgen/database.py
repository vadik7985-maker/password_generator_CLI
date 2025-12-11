"""Модуль для работы с базой данных PostgreSQL."""

import psycopg2
from typing import Optional, List, Tuple, Dict
from .storage import encrypt_password, decrypt_password
from .config import get_db_params


class PasswordDatabase:
    """Класс для управления паролями в базе данных PostgreSQL."""
    
    def __init__(self):
        """Инициализация подключения к БД."""
        self.config = get_db_params()
    
    def _get_connection(self):
        """Устанавливает соединение с БД."""
        return psycopg2.connect(**self.config)
    
    def create_table(self) -> None:
        """Создает таблицу для хранения паролей, если она не существует."""
        query = """
        CREATE TABLE IF NOT EXISTS passwords (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) NOT NULL,
            service VARCHAR(100) NOT NULL,
            encrypted_password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(username, service)
        )
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                conn.commit()
    
    def save_password(self, username: str, service: str, password: str) -> None:
        """Сохраняет пароль в базу данных.
        
        Args:
            username (str): Имя пользователя
            service (str): Название сервиса
            password (str): Пароль в открытом виде
        """
        # Шифруем пароль перед сохранением
        encrypted = encrypt_password(password)
        
        query = """
        INSERT INTO passwords (username, service, encrypted_password)
        VALUES (%s, %s, %s)
        ON CONFLICT (username, service) 
        DO UPDATE SET 
            encrypted_password = EXCLUDED.encrypted_password,
            created_at = CURRENT_TIMESTAMP
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (username, service, encrypted))
                conn.commit()
    
    def get_password(self, username: str, service: str) -> Optional[str]:
        """Получает и расшифровывает пароль.
        
        Args:
            username (str): Имя пользователя
            service (str): Название сервиса
            
        Returns:
            Optional[str]: Пароль в открытом виде или None
        """
        query = """
        SELECT encrypted_password FROM passwords 
        WHERE username = %s AND service = %s
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (username, service))
                result = cur.fetchone()
                if result:
                    encrypted = result[0]
                    return decrypt_password(encrypted)
                return None
    
    def search_by_username(self, username: str) -> List[Tuple[str, str]]:
        """Ищет все записи по имени пользователя.
        
        Args:
            username (str): Имя пользователя
            
        Returns:
            List[Tuple[str, str]]: Список (сервис, пароль в открытом виде)
        """
        query = """
        SELECT service, encrypted_password FROM passwords 
        WHERE username = %s
        ORDER BY service
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (username,))
                results = []
                for service, encrypted in cur.fetchall():
                    try:
                        password = decrypt_password(encrypted)
                        results.append((service, password))
                    except Exception:
                        results.append((service, "[Ошибка расшифровки]"))
                return results
    
    def search_by_service(self, service: str) -> List[Tuple[str, str]]:
        """Ищет все записи по названию сервиса.
        
        Args:
            service (str): Название сервиса
            
        Returns:
            List[Tuple[str, str]]: Список (имя пользователя, пароль в открытом виде)
        """
        query = """
        SELECT username, encrypted_password FROM passwords 
        WHERE service = %s
        ORDER BY username
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (service,))
                results = []
                for username, encrypted in cur.fetchall():
                    try:
                        password = decrypt_password(encrypted)
                        results.append((username, password))
                    except Exception:
                        results.append((username, "[Ошибка расшифровки]"))
                return results
    
    def get_all_records(self) -> List[Dict[str, str]]:
        """Возвращает все записи из БД с расшифрованными паролями.
        
        Returns:
            List[Dict[str, str]]: Список записей
        """
        query = """
        SELECT username, service, encrypted_password, created_at 
        FROM passwords 
        ORDER BY username, service
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                results = []
                for username, service, encrypted, created_at in cur.fetchall():
                    try:
                        password = decrypt_password(encrypted)
                        results.append({
                            'username': username,
                            'service': service,
                            'password': password,
                            'created_at': created_at
                        })
                    except Exception:
                        results.append({
                            'username': username,
                            'service': service,
                            'password': "[Ошибка расшифровки]",
                            'created_at': created_at
                        })
                return results