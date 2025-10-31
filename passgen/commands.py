from .generator import generate_password
from .utils import validate_args
from .storage import save_password, load_passwords, hash_password


def handle_commands(args) -> None:
    """
    Основная логика обработки команд с параметрами из argparse.

    Args:
        args (Namespace): Объект с аргументами командной строки.
    """
    # Обработка поиска пароля
    if args.find:
        if not args.find_file:
            print("При поиске пароля требуется указать --find-file")
            return

        searched_hash = hash_password(args.find)

        try:
            saved_passwords = load_passwords(args.find_file)
        except FileNotFoundError:
            print(f"Файл {args.find_file} не найден.")
            return

        if searched_hash in saved_passwords:
            print("Пароль найден в файле.")
        else:
            print("Пароль в файле не найден.")
        return

    # Обработка генерации пароля
    if not args.find:
        try:
            validate_args(args.length, args.special, args.digits, args.uppercase)
        except ValueError as ve:
            print(f"Ошибка параметров: {ve}")
            return

        try:
            password = generate_password(
                args.length, args.special, args.digits, args.uppercase
            )
        except ValueError as ve:
            print(f"Ошибка генерации пароля: {ve}")
            return
        print(f"Сгенерированный пароль: {password}")

        if args.output:
            save_password(password, args.output)
            print(f"Пароль сохранен в файл: {args.output}")
