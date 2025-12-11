"""Модуль обработки командной строки."""

from .generator import generate_password
from .utils import validate_args
from .database import PasswordDatabase


def handle_commands(args: any) -> None:
    """Обрабатывает команды из аргументов командной строки."""
    
    # Инициализация БД
    try:
        db = PasswordDatabase()
        db.create_table()
    except Exception as e:
        print(f"Ошибка подключения к БД: {e}")
        print("Проверьте параметры в config.py")
        return
    
    # Сохранение пароля в БД
    if args.save:
        try:
            parts = args.save.split(":")
            if len(parts) != 3:
                print("Ошибка: неверный формат. Используйте: username:service:пароль")
                return
                
            username, service, password = parts
            username = username.strip()
            service = service.strip()
            password = password.strip()
            
            db.save_password(username, service, password)
            print(f"Пароль сохранен!")
            print(f"Пользователь: {username}")
            print(f"Сервис:       {service}")
            
        except Exception as e:
            print(f"Ошибка сохранения: {e}")
        return
    
    # Поиск по имени пользователя
    if args.find_by_username:
        try:
            username = args.find_by_username.strip()
            records = db.search_by_username(username)
            
            if records:
                print(f"\nНайдено паролей для пользователя '{username}': {len(records)}")
                print("=" * 60)
                for i, (service, password) in enumerate(records, 1):
                    print(f"{i}. Сервис: {service}")
                    print(f"     Пароль: {password}")
                    if i < len(records):
                        print("-" * 40)
            else:
                print(f"Пароли для пользователя '{username}' не найдены")
                
        except Exception as e:
            print(f"Ошибка поиска: {e}")
        return
    
    # Поиск по сервису
    if args.find_by_service:
        try:
            service = args.find_by_service.strip()
            records = db.search_by_service(service)
            
            if records:
                print(f"\nНайдено паролей для сервиса '{service}': {len(records)}")
                print("=" * 60)
                for i, (username, password) in enumerate(records, 1):
                    print(f"{i}. Пользователь: {username}")
                    print(f"     Пароль:       {password}")
                    if i < len(records):
                        print("-" * 40)
            else:
                print(f"Пароли для сервиса '{service}' не найдены")
                
        except Exception as e:
            print(f"Ошибка поиска: {e}")
        return
    
    # Поиск по имени и сервису
    if args.find_by_both:
        try:
            parts = args.find_by_both.split(":")
            if len(parts) != 2:
                print("Ошибка: неверный формат. Используйте: username:service")
                return
                
            username, service = parts
            username = username.strip()
            service = service.strip()
            
            password = db.get_password(username, service)
            
            if password:
                print(f"\nНайден пароль:")
                print("=" * 40)
                print(f"Пользователь: {username}")
                print(f"Сервис:       {service}")
                print(f"Пароль:       {password}")
            else:
                print(f"Пароль для '{username}' на сервисе '{service}' не найден")
                
        except Exception as e:
            print(f"Ошибка поиска: {e}")
        return
    
    # Показать все записи
    if args.show_all:
        try:
            records = db.get_all_records()
            
            if records:
                print(f"\nВсего записей в базе: {len(records)}")
                print("=" * 60)
                
                for i, record in enumerate(records, 1):
                    print(f"Запись #{i}:")
                    print(f"  Пользователь: {record['username']}")
                    print(f"  Сервис:       {record['service']}")
                    print(f"  Пароль:       {record['password']}")
                    print(f"  Создано:      {record['created_at']}")
                    
                    if i < len(records):
                        print("-" * 60)
            else:
                print("База данных пуста")
                
        except Exception as e:
            print(f"Ошибка получения данных: {e}")
        return
    
    # Генерация пароля
    if args.generate:
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
            print(f"Ошибка генерации: {ve}")
            return
        
        print(f"\nСгенерирован пароль:")
        print("=" * 40)
        print(f"Пароль: {password}")
        print(f"Длина:  {len(password)} символов")
        
        # Предложить сохранить
        print("\nХотите сохранить этот пароль в БД? (y/n): ", end="")
        if input().lower() == 'y':
            print("Введите данные в формате 'пользователь:сервис': ", end="")
            user_service = input().strip()
            
            if ":" in user_service:
                username, service = user_service.split(":", 1)
                username = username.strip()
                service = service.strip()
                
                if username and service:
                    try:
                        db.save_password(username, service, password)
                        print(f"Пароль сохранен!")
                        print(f"Пользователь: {username}")
                        print(f"Сервис:       {service}")
                    except Exception as e:
                        print(f"Ошибка сохранения: {e}")
                else:
                    print("Имя пользователя и сервис не могут быть пустыми")
            else:
                print("Неверный формат. Используйте: пользователь:сервис")