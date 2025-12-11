"""Пакет passgen — генератор и менеджер безопасных паролей."""

from .generator import generate_password
from .utils import validate_args
from .storage import encrypt_password, decrypt_password
from .commands import handle_commands
from .database import PasswordDatabase

__all__ = [
    'generate_password',
    'validate_args',
    'encrypt_password',
    'decrypt_password',
    'handle_commands',
    'PasswordDatabase'
]