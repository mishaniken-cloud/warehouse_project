from dataclasses import dataclass

@dataclass
class Supplier:
    id: int
    name: str
    contact: str | None = None