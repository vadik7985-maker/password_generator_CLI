"""Точка входа CLI-утилиты passgen."""

import argparse
from passgen.commands import handle_commands


def main() -> None:
    """Запускает CLI-утилиту генератора паролей."""
    parser = argparse.ArgumentParser(
        description=f"{30 * '-'} Генератор паролей CLI {30 * '-'}",
        epilog="-" * 83 
    )
    
    # Группа для генерации пароля
    gen_group = parser.add_argument_group("Генерация пароля")
    gen_group.add_argument(
        "-g", "--generate", action="store_true",
        help="Сгенерировать новый пароль"
    )
    gen_group.add_argument(
        "-l", "--length", type=int, default=12,
        help="Длина пароля (по умолчанию %(default)s)"
    )
    gen_group.add_argument(
        "-s", "--special", action="store_true",
        help="Включать спецсимволы"
    )
    gen_group.add_argument(
        "-d", "--digits", action="store_true",
        help="Включать цифры"
    )
    gen_group.add_argument(
        "-u", "--uppercase", action="store_true",
        help="Включать заглавные буквы"
    )
    
    # Группа для сохранения пароля
    save_group = parser.add_argument_group("Сохранение пароля")
    save_group.add_argument(
        "--save", type=str, metavar="'username:service:password'",
        help="Сохранить пароль в БД. Формат: --save 'ivan:gmail:MyPass123'"
    )
    
    # Группа для поиска
    find_group = parser.add_argument_group("Поиск паролей")
    find_group.add_argument(
        "--find-by-username", type=str, metavar="'username'",
        help="Найти все пароли для указанного пользователя"
    )
    find_group.add_argument(
        "--find-by-service", type=str, metavar="'service'",
        help="Найти все пароли для указанного сервиса"
    )
    find_group.add_argument(
        "--find-by-both", type=str, metavar="'username:service'",
        help="Найти пароль по имени и сервису. Формат: --find-by-both 'ivan:gmail'"
    )
    
    # Группа для отображения
    display_group = parser.add_argument_group("Отображение данных")
    display_group.add_argument(
        "--show-all", action="store_true",
        help="Показать все записи из базы данных"
    )

    args = parser.parse_args()
    
    # Проверка формата аргументов
    if args.save and ":" not in args.save:
        parser.error(
            "Формат аргумента --save должен быть: 'username:service:пароль'\n"
            "Пример: --save 'ivan:gmail:MyPassword123'"
        )
    
    if args.find_by_both and ":" not in args.find_by_both:
        parser.error(
            "Формат аргумента --find-by-both должен быть: 'username:service'\n"
            "Пример: --find-by-both 'ivan:gmail'"
        )
    
    # Проверка, что передана хотя бы одна команда
    if not any([args.generate, args.save, args.find_by_username, 
                args.find_by_service, args.find_by_both, args.show_all]):
        parser.print_help()
        return

    handle_commands(args)


if __name__ == "__main__":
    main()
    