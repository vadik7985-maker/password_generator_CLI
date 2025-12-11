"""Модуль конфигурации подключения к БД."""

CONFIG = {
    "dbname": "passwords_db",
    "host": "localhost", 
    "port": 5432,
    "user": "postgres",
    "password": "postgre_471"
}


def get_db_params() -> dict:
    """Возвращает параметры подключения к БД."""
    return CONFIG.copy()