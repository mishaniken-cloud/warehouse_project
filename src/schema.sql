-- schema.sql

-- Включаем поддержку внешних ключей в SQLite
PRAGMA foreign_keys = ON;

-- 1. Удаление старых таблиц (в обратном порядке создания)
DROP TABLE IF EXISTS Operation;
DROP TABLE IF EXISTS Batch;
DROP TABLE IF EXISTS Product;
DROP TABLE IF EXISTS Supplier;
DROP TABLE IF EXISTS Category;

-- 2. Создание таблиц

CREATE TABLE Category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE Supplier (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    contact TEXT
);

CREATE TABLE Product (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category_id INTEGER NOT NULL,
    FOREIGN KEY (category_id) REFERENCES Category(id)
);

CREATE TABLE Batch (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    supplier_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    expiration_date TEXT NOT NULL,
    arrival_date TEXT NOT NULL,
    FOREIGN KEY (product_id) REFERENCES Product(id),
    FOREIGN KEY (supplier_id) REFERENCES Supplier(id)
);

CREATE TABLE Operation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    batch_id INTEGER NOT NULL,
    type TEXT NOT NULL CHECK(type IN ('IN', 'OUT')),
    quantity INTEGER NOT NULL,
    date TEXT NOT NULL,
    FOREIGN KEY (batch_id) REFERENCES Batch(id)
);

-- 3. Добавление тестовых данных

INSERT INTO Category (name) VALUES 
('Молочные продукты'),
('Овощи'),
('Напитки');

INSERT INTO Supplier (name, contact) VALUES 
('Молокозавод №1', '+79001234567'),
('Фермер Иванов', '+79007654321'),
('ООО "Вода"', 'info@water.ru');

INSERT INTO Product (name, category_id) VALUES 
('Молоко 3.2%', 1),
('Помидоры', 2),
('Вода минеральная', 3);

INSERT INTO Batch (product_id, supplier_id, quantity, expiration_date, arrival_date) VALUES 
(1, 1, 100, '2026-11-15', '2026-10-25'),
(2, 2, 50, '2026-11-05', '2026-10-28'),
(3, 3, 200, '2027-10-25', '2026-10-30');

INSERT INTO Operation (batch_id, type, quantity, date) VALUES 
(1, 'IN', 100, '2026-10-25'),
(2, 'IN', 50, '2026-10-28');