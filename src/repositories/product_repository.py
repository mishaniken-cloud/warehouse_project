from database.database import get_connection
from models.product import Product

def _map(row) -> Product:
    return Product(
        id=row['id'], 
        name=row['name'], 
        category_id=row['category_id'],
        category_name=row['category_name']
    )

def get_all() -> list[Product]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.id, p.name, p.category_id, c.name as category_name 
        FROM Product p 
        JOIN Category c ON p.category_id = c.id 
        ORDER BY p.name
    """)
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def get_by_id(product_id: int) -> Product | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.id, p.name, p.category_id, c.name as category_name 
        FROM Product p 
        JOIN Category c ON p.category_id = c.id 
        WHERE p.id = ?
    """, (product_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def create(name: str, category_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Product (name, category_id) VALUES (?, ?)", 
        (name, category_id)
    )
    conn.commit()
    conn.close()
    
def update(product_id: int, name: str, category_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE Product SET name = ?, category_id = ? WHERE id = ?", 
        (name, category_id, product_id)
    )
    conn.commit()
    conn.close()
def delete(product_id: int):
    """Удалить товар"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Product WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()