from repositories import user_repository
from models.user import User

def authenticate(login: str, password: str) -> User | None:
    """
    Проверка логина и пароля пользователя.
    Возвращает объект пользователя, если аутентификация успешна.
    """
    user = user_repository.get_by_login(login)
    
    if user and user.password == password:
        return user
    
    return None

def register(login: str, password: str, name: str, role: str = 'clerk') -> User:
    """
    Регистрация нового пользователя.
    Проверяет корректность данных и отсутствие дублирования логина.
    """
    
    if not login or not login.strip():
        raise Exception("Логин не может быть пустым")
    
    
    if not password or not password.strip():
        raise Exception("Пароль не может быть пустым")
    
    
    if not name or not name.strip():
        raise Exception("Имя не может быть пустым")
    
    
    if role not in ['admin', 'clerk']:
        raise Exception("Недопустимая роль. Доступные роли: admin, clerk")
    
    
    existing_user = user_repository.get_by_login(login)
    if existing_user:
        raise Exception("Пользователь с таким логином уже существует")
    
    
    user_repository.create(login, password, role, name)
    
    
    return user_repository.get_by_login(login)