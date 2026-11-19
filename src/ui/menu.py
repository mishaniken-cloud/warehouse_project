from services.auth_service import authenticate, register
from services.category_service import get_all_categories, create_category
from services.product_service import get_all_products, create_product
from models.user import User

def start_app():
    """Точка входа в приложение"""
    print("="*40)
    print(" СИСТЕМА УЧЕТА СКЛАДА ПРОДУКТОВ")
    print("="*40)
    
    while True:
        print("\n--- ГЛАВНОЕ МЕНЮ ---")
        print("1. Войти в систему")
        print("2. Зарегистрировать нового кладовщика")
        print("0. Выход из программы")
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            user = login_menu()
            if user:
                main_menu(user)
        elif choice == "2":
            register_menu()
        elif choice == "0":
            print("Завершение работы программы...")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

def login_menu() -> User | None:
    print("\n--- АВТОРИЗАЦИЯ ---")
    login_val = input("Логин: ")
    password_val = input("Пароль: ")
    
    try:
        user = authenticate(login_val, password_val)
        if user:
            print(f"\n✅ Успешный вход! Добро пожаловать, {user.name} ({user.role}).")
            return user
        else:
            print("❌ Неверный логин или пароль.")
            return None
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return None

def register_menu():
    print("\n--- РЕГИСТРАЦИЯ НОВОГО ПОЛЬЗОВАТЕЛЯ ---")
    login_val = input("Придумайте логин: ")
    password_val = input("Придумайте пароль: ")
    name_val = input("Ваше ФИО: ")
    
    try:
       
        user = register(login_val, password_val, name_val, role='clerk')
        print(f"✅ Пользователь {user.name} успешно зарегистрирован!")
    except Exception as e:
        print(f"❌ Ошибка регистрации: {e}")

def main_menu(user: User):
    while True:
        print(f"\n--- МЕНЮ ({user.name} | Роль: {user.role}) ---")
        print("1. Посмотреть список категорий")
        print("2. Посмотреть список товаров")
        
        
        if user.role == 'admin':
            print("3. [Админ] Добавить новую категорию")
            print("4. [Админ] Добавить новый товар")
            print("5. [Админ] Изменить название товара")
            print("6. [Админ] Изменить название категории")
            print("7. [Админ] Удалить категорию")
            print("8. [Админ] Удалить товар") 
            
        print("0. Выйти из аккаунта")
        
        choice = input("Выберите действие: ")
        
        try:
            if choice == "1":
                show_categories()
            elif choice == "2":
                show_products()
            elif choice == "3" and user.role == 'admin':
                add_category_ui()
            elif choice == "4" and user.role == 'admin':
                add_product_ui()
            elif choice == "5" and user.role == 'admin':
                edit_product_ui()
            elif choice == "6" and user.role == 'admin':
                edit_category_ui()
            elif choice == "7" and user.role == 'admin':
                delete_category_ui()
            elif choice == "8" and user.role == 'admin':
                delete_product_ui()
            elif choice == "0":
                print("Выход из аккаунта...")
                break
            else:
                print("❌ Неверный выбор или недостаточно прав.")
        except Exception as e:
            print(f"❌ Ошибка при выполнении операции: {e}")

def show_categories():
    categories = get_all_categories()
    print("\n📂 СПИСОК КАТЕГОРИЙ:")
    if not categories:
        print("  (Список пуст)")
    for cat in categories:
        print(f"  ID: {cat.id} | Название: {cat.name}")

def show_products():
    products = get_all_products()
    print("\n📦 СПИСОК ТОВАРОВ:")
    if not products:
        print("  (Список пуст)")
    for prod in products:
        print(f"  ID: {prod.id} | Название: {prod.name} | Категория: {prod.category_name}")

def add_category_ui():
    print("\n--- ДОБАВЛЕНИЕ КАТЕГОРИИ ---")
    name = input("Введите название категории: ")
    try:
        create_category(name)
        print("✅ Категория успешно добавлена!")
    except Exception as e:
        print(f"❌ Ошибка бизнес-логики: {e}")

def add_product_ui():
    print("\n--- ДОБАВЛЕНИЕ ТОВАРА ---")
    name = input("Введите название товара: ")
    
    show_categories()
    
    try:
        cat_id = int(input("Введите ID категории для товара: "))
        create_product(name, cat_id)
        print("✅ Товар успешно добавлен!")
    except ValueError:
        print("❌ Ошибка: ID категории должен быть числом.")
    except Exception as e:
        print(f"❌ Ошибка бизнес-логики: {e}")
def edit_product_ui():
    print("\n--- ИЗМЕНЕНИЕ ТОВАРА ---")
    try:
        prod_id = int(input("Введите ID товара, который нужно изменить: "))
        new_name = input("Введите новое название товара: ")
        
        # Показываем категории, чтобы вспомнить ID
        show_categories()
        cat_id = int(input("Введите ID категории: "))
        
        from services.product_service import update_product
        update_product(prod_id, new_name, cat_id)
        print("✅ Данные товара успешно обновлены!")
    except ValueError:
        print("❌ Ошибка: ID должен быть числом.")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
def edit_category_ui():
    """Изменить название категории"""
    print("\n--- ИЗМЕНЕНИЕ КАТЕГОРИИ ---")
    show_categories()
    
    try:
        cat_id = int(input("Введите ID категории для изменения: "))
        new_name = input("Введите новое название категории: ")
        
        from services.category_service import update_category
        update_category(cat_id, new_name)
        print("✅ Название категории успешно изменено!")
    except ValueError:
        print("❌ Ошибка: ID должен быть числом.")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

def delete_category_ui():
    """Удалить категорию"""
    print("\n--- УДАЛЕНИЕ КАТЕГОРИИ ---")
    show_categories()
    
    try:
        cat_id = int(input("Введите ID категории для удаления: "))
        
        from services.category_service import delete_category
        delete_category(cat_id)
        print("✅ Категория успешно удалена!")
    except ValueError:
        print("❌ Ошибка: ID должен быть числом.")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

def delete_product_ui():
    """Удалить товар"""
    print("\n--- УДАЛЕНИЕ ТОВАРА ---")
    show_products()
    
    try:
        prod_id = int(input("Введите ID товара для удаления: "))
        
        from services.product_service import delete_product
        delete_product(prod_id)
        print("✅ Товар успешно удален!")
    except ValueError:
        print("❌ Ошибка: ID должен быть числом.")
    except Exception as e:
        print(f"❌ Ошибка: {e}")