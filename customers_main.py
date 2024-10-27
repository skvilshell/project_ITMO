from customers_modules import view_events, cancel_ticket

def customer_main_menu():
    """Функция для отображения главного меню для клиента и выполнения действий."""
    while True:
        print("\nЧто вы хотите сделать?")
        print("1. Посмотреть список доступных спектаклей")
        print("2. Отменить покупку билета")
        print("3. Выйти из программы")
        
        choice = input("Введите номер действия (1, 2 или 3): ")
        
        if choice == '1':
            view_events()
        elif choice == '2':
            cancel_ticket()
        elif choice == '3':
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Попробуйте еще раз.")

# Запуск меню для клиента
if __name__ == "__main__":
    customer_main_menu()