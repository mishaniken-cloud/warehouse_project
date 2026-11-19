from database.database import get_connection
from models.operation import Operation

def _map(row) -> Operation:
    return Operation(
        id=row['id'],
        batch_id=row['batch_id'],
        type=row['type'],
        quantity=row['quantity'],
        date=row['date']
    )

def get_all() -> list[Operation]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Operation ORDER BY date DESC")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def create(batch_id: int, type: str, quantity: int, date: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Operation (batch_id, type, quantity, date) VALUES (?, ?, ?, ?)",
        (batch_id, type, quantity, date)
    )
    conn.commit()
    conn.close()