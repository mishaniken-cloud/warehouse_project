import sqlite3
import os

# Путь к файлу базы данных
DB_NAME = 'warehouse.db'
# Путь к SQL скрипту (ищем в той же папке, где лежит main.py)
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), 'schema.sql')

def init_db():
    """Инициализация базы данных и создание таблиц"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Читаем SQL скрипт
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        sql_script = f.read()
        
    # Выполняем скрипт
    cursor.executescript(sql_script)
    
    conn.commit()
    print("База данных успешно создана и заполнена тестовыми данными!")
    
    # Проверка: выведем список товаров
    cursor.execute("SELECT p.name, c.name FROM Product p JOIN Category c ON p.category_id = c.id")
    print("\n--- Список товаров на складе ---")
    for row in cursor.fetchall():
        print(f"Товар: {row[0]} | Категория: {row[1]}")
        
    conn.close()

if __name__ == "__main__":
    print("Система учета склада продуктов запущена.")
    init_db()