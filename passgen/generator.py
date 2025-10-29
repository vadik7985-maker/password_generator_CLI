import secrets
import string


def generate_password(
    length: int = 12,
    use_special: bool = True,
    use_digits: bool = True,
    use_uppercase: bool = True
) -> str:
    """
    Генерирует безопасный пароль.

    Args:
        length (int): Длина пароля.
        use_special (bool): Включать ли спецсимволы.
        use_digits (bool): Включать ли цифры.
        use_uppercase (bool): Включать ли заглавные буквы.

    Returns:
        str: Сгенерированный пароль.

    Raises:
        ValueError: Если не выбран ни один тип символов.
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
