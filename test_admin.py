import pytest
import sqlite3
from admin_modules import (
    add_event,
    delete_event,
    get_current_events,
    get_all_customers,
    get_customers_for_event,
    get_customers_not_for_event,
    get_events_ranked_by_tickets,
    get_events_ranked_by_revenue,
)

@pytest.fixture(scope='function')
def db_connection():
    """Создает временную базу данных для тестирования."""
    connection = sqlite3.connect(':memory:')  # Используем in-memory базу данных для изоляции тестов
    cursor = connection.cursor()
    
    # Создаем необходимые таблицы в базе данных
    cursor.execute('''
        CREATE TABLE events (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            date TEXT NOT NULL,
            free_slots INTEGER NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE customers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER,
            email TEXT,
            phone TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            event_id INTEGER,
            event_name TEXT,
            event_price REAL,
            FOREIGN KEY (customer_id) REFERENCES customers(id),
            FOREIGN KEY (event_id) REFERENCES events(id)
        )
    ''')
    
    connection.commit()  # Зафиксируем изменения в базе данных
    yield connection  # Возвращаем соединение для использования в тестах
    connection.close()  # Закрываем соединение после завершения всех тестов

def test_add_event(db_connection):
    """Тест для функции add_event - добавляет событие в базу данных."""
    add_event(db_connection, "Test Event", 100.0, "2024-11-01", 5)  # Вызываем функцию для добавления события

    cursor = db_connection.cursor()  # Получаем курсор для выполнения SQL-запросов
    cursor.execute("SELECT * FROM events WHERE name = 'Test Event'")  # Запрашиваем добавленное событие
    event = cursor.fetchone()  # Получаем первую строку результата запроса

    # Проверяем, что событие было успешно добавлено
    assert event is not None  
    assert event[1] == "Test Event"  # Проверяем название события
    assert event[2] == 100.0  # Проверяем цену события

def test_delete_event(db_connection):
    """Тест для функции delete_event - удаляет событие из базы данных."""
    add_event(db_connection, "Test Event", 100.0, "2024-11-01", 5)  # Добавляем событие перед удалением

    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM events WHERE name = 'Test Event'")  # Запрашиваем добавленное событие
    event = cursor.fetchone()  # Получаем событие

    # Убедимся, что событие было добавлено успешно
    assert event is not None  
    event_id = event[0]  # Сохраняем ID события для удаления

    delete_event(db_connection, event_id)  # Вызываем функцию для удаления события

    cursor.execute("SELECT * FROM events WHERE id = ?", (event_id,))  # Проверяем, что событие было удалено
    event_after_deletion = cursor.fetchone()  # Получаем результат запроса

    assert event_after_deletion is None  # Убедимся, что событие отсутствует в базе данных

def test_get_current_events(db_connection):
    """Тест для функции get_current_events - получает список актуальных спектаклей."""
    add_event(db_connection, "Current Event", 100.0, "2024-11-01", 5)  # Добавляем актуальное событие
    add_event(db_connection, "Expired Event", 50.0, "2020-01-01", 0)  # Добавляем неактуальное событие

    events = get_current_events(db_connection)  # Вызываем функцию для получения актуальных событий

    assert len(events) == 1  # Проверяем, что возвращено только одно актуальное событие
    assert events[0][1] == "Current Event"  # Проверяем название актуального события

def test_get_all_customers(db_connection):
    """Тест для функции get_all_customers - получает список всех покупателей."""
    cursor = db_connection.cursor()
    cursor.execute("INSERT INTO customers (name, age, email, phone) VALUES (?, ?, ?, ?)", ("John Doe", 30, "john@example.com", "1234567890"))
    db_connection.commit()  # Зафиксируем изменения

    customers = get_all_customers(db_connection)  # Вызываем функцию для получения всех покупателей

    assert len(customers) == 1  # Проверяем, что возвращен один покупатель
    assert customers[0][1] == "John Doe"  # Проверяем имя покупателя

def test_get_customers_for_event(db_connection):
    """Тест для функции get_customers_for_event - получает покупателей для конкретного события."""
    cursor = db_connection.cursor()
    add_event(db_connection, "Test Event", 100.0, "2024-11-01", 5)  # Добавляем тестовое событие

    cursor.execute("INSERT INTO customers (name, age, email, phone) VALUES (?, ?, ?, ?)", ("John Doe", 30, "john@example.com", "1234567890"))
    cursor.execute("INSERT INTO orders (customer_id, event_id) VALUES (?, ?)", (1, 1))  # Добавляем заказ для события
    db_connection.commit()

    customers = get_customers_for_event(db_connection, 1)  # Получаем покупателей для события с ID 1

    assert len(customers) == 1  # Проверяем, что покупатель присутствует
    assert customers[0][1] == "John Doe"  # Проверяем имя покупателя

def test_get_customers_not_for_event(db_connection):
    """Тест для функции get_customers_not_for_event - получает покупателей, не зарегистрированных на событие."""
    cursor = db_connection.cursor()
    add_event(db_connection, "Test Event", 100.0, "2024-11-01", 5)  # Добавляем тестовое событие
    
    cursor.execute("INSERT INTO customers (name, age, email, phone) VALUES (?, ?, ?, ?)", ("John Doe", 30, "john@example.com", "1234567890"))
    cursor.execute("INSERT INTO orders (customer_id, event_id) VALUES (?, ?)", (1, 1))  # Добавляем заказ для события
    
    cursor.execute("INSERT INTO customers (name, age, email, phone) VALUES (?, ?, ?, ?)", ("Jane Doe", 25, "jane@example.com", "0987654321"))
    db_connection.commit()

    customers = get_customers_not_for_event(db_connection, 1)  # Получаем покупателей, не зарегистрированных на событие с ID 1

    assert len(customers) == 1  # Проверяем, что только один покупатель не зарегистрирован
    assert customers[0][1] == "Jane Doe"  # Проверяем имя покупателя

def test_get_events_ranked_by_tickets(db_connection):
    """Тест для функции get_events_ranked_by_tickets - получает события, ранжированные по количеству проданных билетов."""
    add_event(db_connection, "Highly Popular Event", 100.0, "2024-11-01", 5)  # Добавляем популярное событие

    cursor = db_connection.cursor()
    cursor.execute("INSERT INTO customers (name, age, email, phone) VALUES (?, ?, ?, ?)", ("John Doe", 30, "john@example.com", "1234567890"))
    cursor.execute("INSERT INTO orders (customer_id, event_id) VALUES (?, ?)", (1, 1))  # Добавляем заказ
    db_connection.commit()

    ranked_events = get_events_ranked_by_tickets(db_connection)  # Получаем события, ранжированные по билетам

    assert len(ranked_events) == 1  # Проверяем, что возвращено одно событие
    assert ranked_events[0][0] == "Highly Popular Event"  # Проверяем название события

def test_get_events_ranked_by_revenue(db_connection):
    """Тест для функции get_events_ranked_by_revenue - получает события, ранжированные по доходам от продаж билетов."""
    add_event(db_connection, "Test Event", 100.0, "2024-11-01", 5)  # Добавляем событие

    cursor = db_connection.cursor()
    cursor.execute("INSERT INTO customers (name, age, email, phone) VALUES (?, ?, ?, ?)", ("John Doe", 30, "john@example.com", "1234567890"))
    cursor.execute("INSERT INTO orders (customer_id, event_id) VALUES (?, ?)", (1, 1))  # Добавляем заказ
    db_connection.commit()

    ranked_events = get_events_ranked_by_revenue(db_connection)  # Получаем события, ранжированные по доходам

    assert len(ranked_events) == 1  # Проверяем, что возвращено одно событие
    assert ranked_events[0][0] == "Test Event"  # Проверяем название события
