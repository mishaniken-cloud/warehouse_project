from dataclasses import dataclass

@dataclass
class User:
    id: int
    login: str
    password: str
    role: str  # 'admin' или 'clerk'
    name: str