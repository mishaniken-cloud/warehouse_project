from repositories import batch_repository, product_repository, supplier_repository
from models.batch import Batch
from datetime import datetime

def get_all_batches() -> list[Batch]:
    """Получить список всех партий"""
    return batch_repository.get_all()

def get_batch_by_id(batch_id: int) -> Batch | None:
    """Получить партию по ID"""
    return batch_repository.get_by_id(batch_id)

def create_batch(product_id: int, supplier_id: int, quantity: int, 
                 expiration_date: str, arrival_date: str) -> Batch:
    """
    Создать новую партию товара.
    Проверяет корректность данных и бизнес-правила.
    """
    
    if quantity <= 0:
        raise Exception("Количество должно быть больше нуля")
    
    
    product = product_repository.get_by_id(product_id)
    if not product:
        raise Exception(f"Товар с ID {product_id} не найден")
    
   
    supplier = supplier_repository.get_by_id(supplier_id)
    if not supplier:
        raise Exception(f"Поставщик с ID {supplier_id} не найден")
    
    
    try:
        arrival = datetime.strptime(arrival_date, '%Y-%m-%d')
    except ValueError:
        raise Exception("Неверный формат даты прихода. Используйте ГГГГ-ММ-ДД")
    
   
    try:
        expiration = datetime.strptime(expiration_date, '%Y-%m-%d')
    except ValueError:
        raise Exception("Неверный формат даты истечения срока годности. Используйте ГГГГ-ММ-ДД")
    
    
    if expiration <= arrival:
        raise Exception("Срок годности должен быть позже даты прихода")
    
    
    today = datetime.now()
    if expiration <= today:
        raise Exception("Нельзя добавить партию с истёкшим сроком годности")
    
   
    batch_repository.create(product_id, supplier_id, quantity, expiration_date, arrival_date)
    
  
    return batch_repository.get_by_id(batch_repository.get_all()[-1].id)

def get_expiring_batches(days: int = 7) -> list[Batch]:
    """
    Получить партии, срок годности которых истекает в ближайшие N дней.
    """
    from datetime import timedelta
    
    all_batches = batch_repository.get_all()
    today = datetime.now()
    future_date = today + timedelta(days=days)
    
    expiring = []
    for batch in all_batches:
        try:
            exp_date = datetime.strptime(batch.expiration_date, '%Y-%m-%d')
            if exp_date <= future_date and exp_date >= today:
                expiring.append(batch)
        except ValueError:
            continue
    
    return expiring

def get_available_quantity(product_id: int) -> int:
    """
    Получить доступное количество товара на складе.
    Суммирует все партии товара.
    """
    all_batches = batch_repository.get_all()
    total = 0
    
    for batch in all_batches:
        if batch.product_id == product_id:
            total += batch.quantity
    
    return total