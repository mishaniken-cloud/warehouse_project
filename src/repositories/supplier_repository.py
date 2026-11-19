from database.database import get_connection
from models.supplier import Supplier

def _map(row) -> Supplier:
    return Supplier(
        id=row['id'], 
        name=row['name'], 
        contact=row['contact']
    )

def get_all() -> list[Supplier]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Supplier ORDER BY name")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def get_by_id(supplier_id: int) -> Supplier | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Supplier WHERE id = ?", (supplier_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def create(name: str, contact: str | None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Supplier (name, contact) VALUES (?, ?)", 
        (name, contact)
    )
    conn.commit()
    conn.close()