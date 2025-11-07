"""Точка входа CLI-утилиты passgen.

Парсит аргументы командной строки и передаёт управление в модуль commands.
"""

import argparse
from passgen.commands import handle_commands


def main() -> None:
    """Запускает CLI-утилиту генератора паролей.

    Создаёт парсер аргументов и передаёт их в handle_commands.

    Returns:
        None

    Raises:
        SystemExit: При ошибке парсинга аргументов.
    """
    parser = argparse.ArgumentParser(
        description="Генератор паролей CLI - создавайте и храните безопасные пароли"
    )

    parser.add_argument(
        "-l", "--length", type=int, default=12,
        help="Длина пароля (по умолчанию %(default)s)"
    )
    parser.add_argument(
        "-s", "--special", action="store_true",
        help="Включать спецсимволы"
    )
    parser.add_argument(
        "-d", "--digits", action="store_true",
        help="Включать цифры"
    )
    parser.add_argument(
        "-u", "--uppercase", action="store_true",
        help="Включать заглавные буквы"
    )
    parser.add_argument(
        "-o", "--output", type=str,
        help="Файл для сохранения хэшированного пароля"
    )
    parser.add_argument(
        "--find", type=str,
        help="Пароль для поиска (требуется --find-file)"
    )
    parser.add_argument(
        "--find-file", type=str,
        help="Файл для поиска пароля (обязательно с --find)"
    )

    args = parser.parse_args()

    if args.find and not args.find_file:
        parser.error("--find требует указания --find-file")

    handle_commands(args)


if __name__ == "__main__":
    main()
