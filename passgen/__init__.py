"""Пакет passgen — генератор и менеджер безопасных паролей.

Предоставляет функции для генерации паролей, их хэширования,
сохранения и поиска по хэшу.

Экспортируемые объекты:
    - generate_password
    - validate_args
    - save_password
    - load_passwords
    - hash_password
    - handle_commands
"""

from .generator import generate_password
from .utils import validate_args
from .storage import save_password, load_passwords, hash_password
from .commands import handle_commands
