import pytest
import sqlite3
from unittest import mock
from customers_modules import view_events, register_customer, cancel_ticket, connect_db  # Убедитесь в правильности импорта


@pytest.fixture
def mock_db():
    """Создание тестовой базы данных в памяти и добавление тестовых данных."""
    connection = sqlite3.connect(':memory:')
    cursor = connection.cursor()
    
    cursor.execute('''
        CREATE TABLE customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER NOT NULL,
            customer_id INTEGER NOT NULL,
            event_name TEXT NOT NULL,
            event_price REAL NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE events (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            date TEXT NOT NULL,
            free_slots INTEGER NOT NULL
        )
    ''')
    
    # Добавляем тестовую запись в таблицу событий
    cursor.execute("INSERT INTO events (id, name, price, date, free_slots) VALUES (1, 'Спектакль 1', 100, '2023-10-01', 10)")
    connection.commit()
    
    yield connection
    
    connection.close()


def test_view_events_available(mock_db, capsys):
    """Тестируем функцию view_events для отображения доступных спектаклей."""
    inputs = ['1']  # ID спектакля для выбора
    with mock.patch('builtins.input', side_effect=inputs):
        view_events()

    # Проверяем консольный вывод
    captured = capsys.readouterr()
    assert "Доступные спектакли:" in captured.out
    assert "ID: 1, Название: Спектакль 1, Цена: 100, Дата: 2023-10-01, Свободные места: 10" in captured.out
    assert "Регистрация завершена, билет успешно куплен!" in captured.out


def test_register_customer(mock_db, capsys):
    """Тестируем регистрацию покупателя и создание заказа."""
    inputs = ['Иван', '30', 'ivan@example.com', '1234567890']
    with mock.patch('builtins.input', side_effect=inputs):
        register_customer(event_id=1, event_name='Спектакль 1', event_price=100)

    # Проверяем консольный вывод
    captured = capsys.readouterr()
    assert "Регистрация завершена, билет успешно куплен!" in captured.out

    # Проверяем, что покупатель был добавлен в базу данных
    cursor = mock_db.cursor()
    cursor.execute("SELECT * FROM customers WHERE email = 'ivan@example.com'")
    customer = cursor.fetchone()
    assert customer is not None
    assert customer[1] == 'Иван'  # Проверяем имя
    assert customer[2] == 30  # Проверяем возраст

    # Проверяем, что заказ был добавлен в базу данных
    cursor.execute("SELECT * FROM orders WHERE customer_id = ?", (customer[0],))
    order = cursor.fetchone()
    assert order is not None
    assert order[2] == customer[0]  # customer_id соответствует
    assert order[3] == 'Спектакль 1'  # event_name соответствует
    assert order[4] == 100  # event_price соответствует

    # Проверяем, что количество свободных мест уменьшилось на 1
    cursor.execute("SELECT free_slots FROM events WHERE id = 1")
    free_slots = cursor.fetchone()[0]
    assert free_slots == 9  # 10 - 1 = 9


def test_cancel_ticket(mock_db, capsys):
    """Тестируем отмену заказа."""
    # Сначала регистрируем клиента для создания заказа
    inputs_register = ['Петр', '28', 'petr@example.com', '0987654321']
    with mock.patch('builtins.input', side_effect=inputs_register):
        register_customer(event_id=1, event_name='Спектакль 1', event_price=100)

    # Получаем ID созданного заказа
    cursor = mock_db.cursor()
    cursor.execute("SELECT customer_id FROM customers WHERE email = 'petr@example.com'")
    customer_id = cursor.fetchone()[0]
    cursor.execute("SELECT order_id FROM orders WHERE customer_id = ?", (customer_id,))
    order_id = cursor.fetchone()[0]

    inputs_cancel = [order_id]  # ID заказа для отмены
    with mock.patch('builtins.input', side_effect=inputs_cancel):
        cancel_ticket()

    # Проверяем консольный вывод
    captured = capsys.readouterr()
    assert "Заказ успешно отменен." in captured.out

    # Проверяем, что заказ был удален из базы данных
    cursor.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,))
    order = cursor.fetchone()
    assert order is None

    # Проверяем, что количество свободных мест увеличилось на 1
    cursor.execute("SELECT free_slots FROM events WHERE id = 1")
    free_slots = cursor.fetchone()[0]
    assert free_slots == 10  # 9 + 1 = 10


def test_cancel_nonexistent_ticket(mock_db, capsys):
    """Тестируем отмену несуществующего заказа."""
    inputs = ['999']  # Не существующий номер заказа
    with mock.patch('builtins.input', side_effect=inputs):
        cancel_ticket()
    
    # Проверяем консольный вывод
    captured = capsys.readouterr()
    assert "Заказ с таким номером не найден." in captured.out