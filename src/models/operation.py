from dataclasses import dataclass

@dataclass
class Operation:
    id: int
    batch_id: int
    type: str  # 'IN' или 'OUT'
    quantity: int
    date: str