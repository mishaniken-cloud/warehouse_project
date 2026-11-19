import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.database import init_db
from ui.menu import login_menu, main_menu

def main():
    print("Система учета склада продуктов запущена.")
    
    
    init_db()
    
    
    user = login_menu()
    
    if user:
        main_menu(user)

if __name__ == "__main__":
    main()