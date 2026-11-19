from repositories import product_repository, category_repository
from models.product import Product

def get_all_products() -> list[Product]:
    """Получить список всех товаров"""
    return product_repository.get_all()

def get_product_by_id(product_id: int) -> Product | None:
    """Получить товар по ID"""
    return product_repository.get_by_id(product_id)

def create_product(name: str, category_id: int) -> Product:
    """
    Создать новый товар.
    Проверяет корректность данных и существование категории.
    """
    
    if not name or not name.strip():
        raise Exception("Название товара не может быть пустым")
    
    name = name.strip()
    
    
    category = category_repository.get_by_id(category_id)
    if not category:
        raise Exception(f"Категория с ID {category_id} не найдена")
    
    
    existing_products = product_repository.get_all()
    for product in existing_products:
        if product.name.lower() == name.lower() and product.category_id == category_id:
            raise Exception(f"Товар '{name}' уже существует в категории '{category.name}'")
    
    
    product_repository.create(name, category_id)
    
    
    return product_repository.get_by_id(product_repository.get_all()[-1].id)

def get_products_by_category(category_id: int) -> list[Product]:
    """Получить все товары определённой категории"""
    all_products = product_repository.get_all()
    return [p for p in all_products if p.category_id == category_id]
def update_product(product_id: int, name: str, category_id: int):
    """Обновить товар через сервис"""
    if not name.strip():
        raise Exception("Название товара не может быть пустым")
    
    category = category_repository.get_by_id(category_id)
    if not category:
        raise Exception(f"Категория с ID {category_id} не найдена")
    
    
    existing_product = product_repository.get_by_id(product_id)
    if not existing_product:
        raise Exception(f"Товар с ID {product_id} не найден")
        
    product_repository.update(product_id, name.strip(), category_id)
def delete_product(product_id: int):
    """
    Удалить товар.
    Проверяет, не используется ли товар в партиях.
    """
    
    product = product_repository.get_by_id(product_id)
    if not product:
        raise Exception(f"Товар с ID {product_id} не найден")
    
    
    from repositories import batch_repository
    batches = batch_repository.get_all()
    for batch in batches:
        if batch.product_id == product_id:
            raise Exception(f"Невозможно удалить товар '{product.name}': он используется в партиях")
    
    
    product_repository.delete(product_id)