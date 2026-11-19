from repositories import operation_repository, batch_repository
from models.operation import Operation
from datetime import datetime

def get_all_operations() -> list[Operation]:
    """Получить список всех операций"""
    return operation_repository.get_all()

def create_operation(batch_id: int, type: str, quantity: int, date: str) -> Operation:
    """
    Создать новую операцию (приход или расход).
    Проверяет корректность данных и бизнес-правила.
    """
    
    if type not in ['IN', 'OUT']:
        raise Exception("Недопустимый тип операции. Используйте 'IN' (приход) или 'OUT' (расход)")
    
    
    if quantity <= 0:
        raise Exception("Количество должно быть больше нуля")
    
    
    batch = batch_repository.get_by_id(batch_id)
    if not batch:
        raise Exception(f"Партия с ID {batch_id} не найдена")
    
    
    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        raise Exception("Неверный формат даты. Используйте ГГГГ-ММ-ДД")
    
   
    if type == 'OUT':
        
        all_ops = operation_repository.get_all()
        current_quantity = batch.quantity
        
        
        for op in all_ops:
            if op.batch_id == batch_id:
                if op.type == 'IN':
                    current_quantity += op.quantity
                else:  # OUT
                    current_quantity -= op.quantity
        
        if current_quantity < quantity:
            raise Exception(f"Недостаточно товара на складе. Доступно: {current_quantity}, запрошено: {quantity}")
    
   
    operation_repository.create(batch_id, type, quantity, date)
    
   
    return operation_repository.get_all()[-1]

def get_operations_by_batch(batch_id: int) -> list[Operation]:
    """Получить все операции для конкретной партии"""
    all_ops = operation_repository.get_all()
    return [op for op in all_ops if op.batch_id == batch_id]

def get_current_stock(batch_id: int) -> int:
    """
    Рассчитать текущий остаток партии на складе.
    """
    batch = batch_repository.get_by_id(batch_id)
    if not batch:
        raise Exception(f"Партия с ID {batch_id} не найдена")
    
    
    stock = batch.quantity
    
    
    all_ops = operation_repository.get_all()
    for op in all_ops:
        if op.batch_id == batch_id:
            if op.type == 'IN':
                stock += op.quantity
            else:  # OUT
                stock -= op.quantity
    
    return stock