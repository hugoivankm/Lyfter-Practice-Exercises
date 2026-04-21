SET search_path TO transactions;

INSERT INTO Products (name, current_price, brand, stock_code, stock_quantity) VALUES 
('Ultra-Wide Monitor', 450.00, 'Dell', 'MON-DL-99X', 15),
('Ergonomic Mouse', 65.00, 'Logitech', 'MSE-LG-ERGO', 120),
('Noise Cancelling Headphones', 299.99, 'Sony', 'HDP-SN-1000', 45);

-- Insert a few Users
INSERT INTO Users (full_name, email) VALUES 
('Alice Freeman', 'alice.f@example.com'),
('Bob Vance', 'bob.vance@refrigeration.com');

-- Insert Payment Methods
INSERT INTO Payment_methods (method_type, bank_name, users_id) VALUES 
('credit card', 'Chase Bank', 1),
('paypal', 'PayPal Wallet', 2);


-- Invoice 1
INSERT INTO Invoices (invoice_number, total, payment_methods_id, users_id) 
VALUES (2026001, 515.00, 1, 1);

INSERT INTO Details (price_at_sale, quantity, invoices_id, products_id) VALUES 
(450.00, 1, 1, 1), 
(65.00, 1, 1, 2);


-- Simulate a purchase to for the purchase transaction
INSERT INTO Cart (users_id) VALUES (1);

INSERT INTO Cart_Products (cart_id, products_id, quantity) VALUES 
(1, 1, 1), 
(1, 3, 1);
