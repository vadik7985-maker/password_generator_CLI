"""Модуль генерации безопасных паролей с использованием криптографически стойкого источника.

Использует модуль secrets для генерации случайных символов из выбранного алфавита.
"""

import secrets
import string


def generate_password(
    length: int = 12,
    use_special: bool = True,
    use_digits: bool = True,
    use_uppercase: bool = True
) -> str:
    """Генерирует случайный безопасный пароль заданной длины.

    Args:
        length (int): Длина пароля. По умолчанию 12.
        use_special (bool): Включать ли спецсимволы. По умолчанию True.
        use_digits (bool): Включать ли цифры. По умолчанию True.
        use_uppercase (bool): Включать ли заглавные буквы. По умолчанию True.

    Returns:
        str: Сгенерированный пароль.

    Raises:
        ValueError: Если не выбран ни один тип символов (алфавит пуст).
    """
    alphabet = string.ascii_lowercase
    if use_uppercase:
        alphabet += string.ascii_uppercase
    if use_digits:
        alphabet += string.digits
    if use_special:
        alphabet += string.punctuation

    if not alphabet:
        raise ValueError("Выберите хотя бы один тип символов для генерации")

    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password
