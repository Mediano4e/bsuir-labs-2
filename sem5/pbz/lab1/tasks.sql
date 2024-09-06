-- Задача №24: -- ++++++
SELECT id
FROM suppliers
WHERE status < (SELECT status FROM suppliers WHERE id = 1);

-- Задача №19: --
SELECT DISTINCT p.name
FROM projects p
JOIN quantities q ON p.id = q.project_id
WHERE q.supplier_id = 1;

-- Задача №27: --
SELECT q.supplier_id
FROM quantities q
JOIN (
    SELECT project_id, AVG(quantity) AS avg_quantity
    FROM quantities
    WHERE product_id = 1
    GROUP BY project_id
) avg_q ON q.project_id = avg_q.project_id
WHERE q.product_id = 1
AND q.quantity > avg_q.avg_quantity;

-- Задача №6: --
SELECT q.supplier_id, q.product_id, q.project_id
FROM quantities q
JOIN suppliers s ON q.supplier_id = s.id
JOIN products p ON q.product_id = p.id
JOIN projects pr ON q.project_id = pr.id
WHERE s.city = p.city
AND p.city = pr.city;

-- Задача №1: -- ++++++
SELECT * 
FROM projects;

-- Задача №9: --
SELECT DISTINCT q.product_id
FROM quantities q
JOIN suppliers s ON q.supplier_id = s.id
WHERE s.city = 'Лондон';

-- Задача №13: --
SELECT DISTINCT q.project_id
FROM quantities q
JOIN suppliers s ON q.supplier_id = s.id
JOIN projects p ON q.project_id = p.id
WHERE s.city != p.city;

-- Задача №35: --
SELECT s.id AS supplier_id, p.id AS product_id
FROM suppliers s
CROSS JOIN products p
LEFT JOIN quantities q ON s.id = q.supplier_id AND p.id = q.product_id
WHERE q.supplier_id IS NULL;

-- Задача №18: --
SELECT DISTINCT q.product_id
FROM quantities q
JOIN (
    SELECT project_id, AVG(quantity) AS avg_quantity
    FROM quantities
    GROUP BY project_id
    HAVING AVG(quantity) > 320
) avg_q ON q.project_id = avg_q.project_id;

-- Задача №33: -- ++++++
SELECT city
FROM suppliers
INTERSECT
SELECT city
FROM products
INTERSECT
SELECT city
FROM projects;
