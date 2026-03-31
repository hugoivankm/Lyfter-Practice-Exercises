
INSERT INTO Users (full_name, email) VALUES 
('Alice Johnson', 'alice@example.com'),
('Bob Smith', 'bob@example.com'),
('Charlie Davis', 'charlie@example.com'),
('Diana Prince', 'diana@example.com'),
('Edward Norton', 'edward@example.com');


INSERT INTO Products (name, current_price, entry_date, brand, sku) VALUES 
('iPhone 15', 999.99, '2026-01-10', 'Apple', 1001),
('Galaxy S24', 899.99, '2026-01-12', 'Samsung', 1002),
('Wireless Earbuds', 149.99, '2026-01-15', 'Sony', 1003),
('Mechanical Keyboard', 120.00, '2026-01-20', 'Logitech', 1004),
('Gaming Mouse', 75.50, '2026-01-22', 'Razer', 1005),
('4K Monitor', 350.00, '2026-02-01', 'Dell', 1006),
('USB-C Hub', 45.00, '2026-02-05', 'Anker', 1007),
('Laptop Stand', 30.00, '2026-02-10', 'Rain Design', 1008),
('Webcam 1080p', 80.00, '2026-02-15', 'Logitech', 1009),
('External SSD 1TB', 110.00, '2026-02-20', 'Samsung', 1010),
('Patek Philippe Nautilus', 125000.00, '2026-03-29', 'Patek Philippe', 9001);

INSERT INTO Payment_methods (users_id, method_type, bank_name) VALUES 
(1, 'credit card', 'Chase'),
(2, 'paypal', 'Digital Wallet'),
(3, 'cash', 'Local Branch'),
(4, 'credit card', 'Wells Fargo'),
(5, 'paypal', 'Digital Wallet');

INSERT INTO Invoices (invoice_number, total, payment_methods_id, users_id) VALUES 
(5001, 1149.98, 1, 1),
(5002, 899.99, 2, 2), 
(5003, 150.50, 5, 5);


INSERT INTO Details (price_at_sale, quantity, invoices_id, products_id) VALUES 
(999.99, 1, 1, 1),
(149.99, 1, 1, 3),
(899.99, 1, 2, 2),
(75.50, 2, 3, 5);


INSERT INTO Reviews (comment, rating, users_id, products_id) VALUES 
('Best phone I''ve ever had!', 5, 1, 1),
('A bit expensive but worth it.', 4, 2, 2);


INSERT INTO Cart (users_id) VALUES 
(3),
(4);

INSERT INTO Cart_Products (cart_id, products_id) VALUES 
(1, 4), 
(2, 6);
