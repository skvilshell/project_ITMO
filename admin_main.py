# admin_main.py

from admin_modules import (
    get_current_events, add_event, delete_event, get_all_customers,
    get_customers_for_event, get_customers_not_for_event,
    get_events_ranked_by_tickets, get_events_ranked_by_revenue
)

def admin_main_menu():
    """Главное меню для администратора с командами и справкой."""
    while True:
        print("\nДоступные команды:")
        print("1. Показать список актуальных спектаклей")
        print("2. Добавить спектакль")
        print("3. Удалить спектакль")
        print("4. Показать всех покупателей")
        print("5. Показать покупателей на конкретный спектакль")
        print("6. Показать покупателей, не зарегистрированных на конкретный спектакль")
        print("7. Показать спектакли по количеству проданных билетов")
        print("8. Показать спектакли по сумме полученной за билеты")
        print("9. Выйти из программы")

        choice = input("Введите номер команды (1-9) или 'help' для справки: ")

        if choice == '1':
            events = get_current_events()
            for event in events:
                print(f"ID: {event[0]}, Название: {event[1]}, Цена: {event[2]}, Дата: {event[3]}, Свободные места: {event[4]}")
        
        elif choice == '2':
            name = input("Введите название спектакля: ")
            price = int(input("Введите цену билета: "))
            date = input("Введите дату спектакля (ГГГГ-ММ-ДД): ")
            free_slots = int(input("Введите количество свободных мест: "))
            add_event(name, price, date, free_slots)
        
        elif choice == '3':
            event_id = int(input("Введите ID спектакля для удаления: "))
            delete_event(event_id)
        
        elif choice == '4':
            customers = get_all_customers()
            for customer in customers:
                print(f"ID: {customer[0]}, Имя: {customer[1]}, Возраст: {customer[2]}, Email: {customer[3]}, Телефон: {customer[4]}")
        
        elif choice == '5':
            event_id = int(input("Введите ID спектакля: "))
            customers = get_customers_for_event(event_id)
            for customer in customers:
                print(f"ID: {customer[0]}, Имя: {customer[1]}, Возраст: {customer[2]}, Email: {customer[3]}, Телефон: {customer[4]}")
        
        elif choice == '6':
            event_id = int(input("Введите ID спектакля: "))
            customers = get_customers_not_for_event(event_id)
            for customer in customers:
                print(f"ID: {customer[0]}, Имя: {customer[1]}, Возраст: {customer[2]}, Email: {customer[3]}, Телефон: {customer[4]}")
        
        elif choice == '7':
            events = get_events_ranked_by_tickets()
            for event in events:
                print(f"Название: {event[0]}, Продано билетов: {event[1]}")
        
        elif choice == '8':
            events = get_events_ranked_by_revenue()
            for event in events:
                print(f"Название: {event[0]}, Сумма продаж: {event[1]}")
        
        elif choice == '9':
            print("Выход из программы.")
            break
        
        elif choice.lower() == 'help':
            print("\nВведите номер команды для выполнения действия.")
        else:
            print("Неверная команда. Введите 'help' для справки.")

# Запуск главного меню для администратора
if __name__ == "__main__":
    admin_main_menu()
