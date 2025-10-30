def validate_args(length: int, use_special: bool, use_digits: bool, use_uppercase: bool) -> None:
    """
    Проверяет корректность входных параметров генерации пароля.

    Args:
        length (int): Длина пароля.
        use_special (bool): Использование спецсимволов.
        use_digits (bool): Использование цифр.
        use_uppercase (bool): Использование заглавных букв.

    Raises:
        ValueError: Если длина не положительна.
    """
    if length <= 0:
        raise ValueError("Длина пароля должна быть положительным числом")
    if not (use_special or use_digits or use_uppercase):
        print("Предупреждение: не выбраны спецсимволы, цифры или заглавные буквы. "
              "Будут использоваться только строчные буквы.")
