from dataclasses import dataclass

@dataclass
class Product:
    id: int
    name: str
    category_id: int
    category_name: str | None = None  