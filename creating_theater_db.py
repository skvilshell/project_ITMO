import sqlite3

con = sqlite3.connect('theater.db')
curs = con.cursor()

# Создание таблицы events
curs.execute('''
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price INTEGER NOT NULL,
    date TEXT NOT NULL,
    free_slots INTEGER NOT NULL)
''')

# Создание таблицы customers
curs.execute('''
CREATE TABLE IF NOT EXISTS customers(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    email TEXT UNIQUE,
    phone TEXT NOT NULL)
''')

# Включение поддержки внешних ключей
curs.execute("PRAGMA foreign_keys = ON")

# Создание таблицы orders
curs.execute('''
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER,
    customer_id INTEGER,
    event_name TEXT,
    event_price INTEGER,
    FOREIGN KEY (event_id) REFERENCES events(id),
    FOREIGN KEY (customer_id) REFERENCES customers(id)
)
''')

#Добавление спектаклей в таблицу events
events = [
    ('Гамлет', 1000, '2024.12.14', 100),
    ('Чайка', 1500, '2024.12.15', 100),
    ('На дне', 2000, '2024.12.16', 100)
]

curs.executemany('''
    INSERT INTO events (name, price, date, free_slots)
    VALUES (?, ?, ?, ?)
''', events)

con.commit()
con.close()
print('База данных успешно создана')