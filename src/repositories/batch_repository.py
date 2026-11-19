from database.database import get_connection
from models.batch import Batch

def _map(row) -> Batch:
    return Batch(
        id=row['id'],
        product_id=row['product_id'],
        supplier_id=row['supplier_id'],
        quantity=row['quantity'],
        expiration_date=row['expiration_date'],
        arrival_date=row['arrival_date'],
        product_name=row['product_name'],
        supplier_name=row['supplier_name']
    )

def get_all() -> list[Batch]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT b.id, b.product_id, b.supplier_id, b.quantity, 
               b.expiration_date, b.arrival_date, 
               p.name as product_name, s.name as supplier_name
        FROM Batch b
        JOIN Product p ON b.product_id = p.id
        JOIN Supplier s ON b.supplier_id = s.id
        ORDER BY b.arrival_date DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def get_by_id(batch_id: int) -> Batch | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT b.id, b.product_id, b.supplier_id, b.quantity, 
               b.expiration_date, b.arrival_date, 
               p.name as product_name, s.name as supplier_name
        FROM Batch b
        JOIN Product p ON b.product_id = p.id
        JOIN Supplier s ON b.supplier_id = s.id
        WHERE b.id = ?
    """, (batch_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def create(product_id: int, supplier_id: int, quantity: int, expiration_date: str, arrival_date: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Batch (product_id, supplier_id, quantity, expiration_date, arrival_date) 
        VALUES (?, ?, ?, ?, ?)
    """, (product_id, supplier_id, quantity, expiration_date, arrival_date))
    conn.commit()
    conn.close()