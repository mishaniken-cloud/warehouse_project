import sqlite3
import os

DB_NAME = 'warehouse.db'

def get_connection():
    """Получить подключение к базе данных"""
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), DB_NAME)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  
    return conn

def init_db():
    """Инициализация базы данных из schema.sql"""
    conn = get_connection()
    cursor = conn.cursor()
    
    schema_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'schema.sql')
    
    with open(schema_path, 'r', encoding='utf-8') as f:
        sql_script = f.read()
    
    cursor.executescript(sql_script)
    conn.commit()
    conn.close()
    print("База данных инициализирована!")