from repositories import category_repository
from models.category import Category

def get_all_categories() -> list[Category]:
    """Получить список всех категорий"""
    return category_repository.get_all()

def get_category_by_id(category_id: int) -> Category | None:
    """Получить категорию по ID"""
    return category_repository.get_by_id(category_id)

def create_category(name: str) -> Category:
    """
    Создать новую категорию.
    Проверяет корректность имени и отсутствие дубликатов.
    """
    
    if not name or not name.strip():
        raise Exception("Название категории не может быть пустым")
    
    name = name.strip()
    
    
    existing_categories = category_repository.get_all()
    for cat in existing_categories:
        if cat.name.lower() == name.lower():
            raise Exception(f"Категория '{name}' уже существует")
    
    
    category_repository.create(name)
    
    
    return category_repository.get_by_id(category_repository.get_all()[-1].id)

def delete_category(category_id: int):
    """
    Удалить категорию.
    Проверяет, не используется ли категория в товарах.
    """
    
    category = category_repository.get_by_id(category_id)
    if not category:
        raise Exception("Категория не найдена")
    
   
    from repositories import product_repository
    products = product_repository.get_all()
    for product in products:
        if product.category_id == category_id:
            raise Exception(f"Невозможно удалить категорию '{category.name}': она используется в товаре '{product.name}'")
    
    
    category_repository.delete(category_id)
def update_category(category_id: int, new_name: str):
    """
    Изменить название категории.
    Проверяет корректность имени и отсутствие дубликатов.
    """
   
    if not new_name or not new_name.strip():
        raise Exception("Название категории не может быть пустым")
    
    new_name = new_name.strip()
    
   
    category = category_repository.get_by_id(category_id)
    if not category:
        raise Exception(f"Категория с ID {category_id} не найдена")
    
    
    existing_categories = category_repository.get_all()
    for cat in existing_categories:
        if cat.id != category_id and cat.name.lower() == new_name.lower():
            raise Exception(f"Категория '{new_name}' уже существует")
    
    
    category_repository.update(category_id, new_name)