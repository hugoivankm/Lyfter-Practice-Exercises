SELECT * FROM Products;

SELECT * FROM Products
WHERE current_price > 50000;

--
SELECT
    p.name AS product_name,
    i.id AS invoices_id
FROM Details d
JOIN Invoices i ON d.invoices_id = i.id
JOIN Products p ON d.products_id = p.id
WHERE d.products_id = 1;

--
SELECT
    p.id AS product_id,
    p.name AS product_name,
    SUM(d.quantity) AS total_units_sold,
    SUM(d.quantity * d.price_at_sale) AS item_total,
    COUNT(d.invoices_id) AS number_of_orders
FROM Details d
JOIN Invoices i ON d.invoices_id = i.id
JOIN Products p ON d.products_id = p.id
GROUP BY p.id, p.name
ORDER BY item_total DESC;

--
SELECT
    u.full_name AS user_name,
    u.email AS email,
    i.invoice_number AS invoice_number
FROM Invoices i
JOIN Payment_methods pm ON pm.id = i.payment_methods_id
JOIN Users u ON u.id = pm.users_id
WHERE u.id = 1;

--
SELECT 
    invoice_number,
    total
FROM Invoices
ORDER BY total DESC;

--
SELECT DISTINCT invoice_number
FROM Invoices;
