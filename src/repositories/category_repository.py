from database.database import get_connection
from models.category import Category

def _map(row) -> Category:
    """Преобразовать строку из БД в объект Category"""
    return Category(
        id=row['id'],
        name=row['name']
    )

def create(name: str):
    """Создать новую категорию"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO Category (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

def get_all() -> list[Category]:
    """Получить все категории"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Category ORDER BY name")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def get_by_id(category_id: int) -> Category | None:
    """Получить категорию по ID"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Category WHERE id = ?", (category_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def delete(category_id: int):
    """Удалить категорию"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Category WHERE id = ?", (category_id,))
    conn.commit()
    conn.close()