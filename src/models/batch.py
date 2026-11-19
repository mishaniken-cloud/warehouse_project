from dataclasses import dataclass

@dataclass
class Batch:
    id: int
    product_id: int
    supplier_id: int
    quantity: int
    expiration_date: str
    arrival_date: str
    product_name: str | None = None  
    supplier_name: str | None = None  