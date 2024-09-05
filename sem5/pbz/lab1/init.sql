CREATE TABLE suppliers (
    id SERIAL PRIMARY KEY NOT NULL,
    name VARCHAR(30) NOT NULL,
    status INTEGER NOT NULL,
    city VARCHAR(30) NOT NULL
);

INSERT INTO suppliers(name, status, city)
VALUES 
    ('Петров', 20, 'Москва'),
    ('Синицин', 10, 'Таллинн'),
    ('Федоров', 30, 'Таллинн'),
    ('Чаянов', 20, 'Минск'),
    ('Крюков', 30, 'Киев');

------------------------------------------------

CREATE TABLE products (
    id SERIAL PRIMARY KEY NOT NULL,
    name VARCHAR(30) NOT NULL,
    color VARCHAR(30) NOT NULL,
    size INTEGER NOT NULL,
    city VARCHAR(30) NOT NULL
);

INSERT INTO products(name, color, size, city)
VALUES 
    ('Болт', 'Красный', 12, 'Москва'),
    ('Гайка', 'Зеленый', 17, 'Минск'),
    ('Диск', 'Черный', 17, 'Вильнюс'),
    ('Диск', 'Черный', 14, 'Москва'),
    ('Корпус', 'Красный', 12, 'Минск'),
    ('Крышки', 'Красный', 19, 'Москва');

------------------------------------------------

CREATE TABLE projects (
    id SERIAL PRIMARY KEY NOT NULL,
    name VARCHAR(30) NOT NULL,
    city VARCHAR(30) NOT NULL
);

INSERT INTO projects(name, city)
VALUES 
    ('ИПР1', 'Минск'),
    ('ИПР2', 'Таллинн'),
    ('ИПР3', 'Псков'),
    ('ИПР4', 'Псков'),
    ('ИПР5', 'Москва'),
    ('ИПР6', 'Саратов'),
    ('ИПР7', 'Москва');

------------------------------------------------

CREATE TABLE quantities (
    supplier_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    project_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id),
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);


INSERT INTO quantities(supplier_id, product_id, project_id, quantity)
VALUES 
    (1, 1, 1, 200),
    (1, 1, 2, 700),
    (2, 3, 1, 400),
    (2, 2, 2, 200),
    (2, 3, 3, 200),
    (2, 3, 4, 500),
    (2, 3, 5, 600),
    (2, 3, 6, 400),
    (2, 3, 7, 800),
    (2, 5, 2, 100),
    (3, 3, 1, 200),
    (3, 4, 2, 500),
    (4, 6, 3, 300),
    (4, 6, 7, 300),
    (5, 2, 2, 200),
    (5, 2, 4, 100),
    (5, 5, 5, 500),
    (5, 5, 7, 100),
    (5, 6, 2, 200),
    (5, 1, 2, 100),
    (5, 3, 4, 200),
    (5, 4, 4, 800),
    (5, 5, 4, 400),
    (5, 6, 4, 500);
