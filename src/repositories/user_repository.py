from database.database import get_connection
from models.user import User

def _map(row) -> User:
    """Преобразует строку из базы данных в объект User"""
    return User(
        id=row['id'],
        login=row['login'],
        password=row['password'],
        role=row['role'],
        name=row['name']
    )

def get_by_login(login: str) -> User | None:
    """Найти пользователя по логину"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM User WHERE login = ?", (login,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def get_by_id(user_id: int) -> User | None:
    """Найти пользователя по ID"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM User WHERE id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def create(login: str, password: str, role: str, name: str):
    """Создать нового пользователя"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO User (login, password, role, name) VALUES (?, ?, ?, ?)",
        (login, password, role, name)
    )
    conn.commit()
    conn.close()