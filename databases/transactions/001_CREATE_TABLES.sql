SET search_path TO transactions;


DROP TABLE IF EXISTS Cart_Products;

DROP TABLE IF EXISTS Cart;

DROP TABLE IF EXISTS Details;

DROP TABLE IF EXISTS Invoices;

DROP TABLE IF EXISTS Products;

DROP TABLE IF EXISTS Payment_methods;

DROP TABLE IF EXISTS Users;

CREATE TABLE Users (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    registration_day TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Payment_methods (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    method_type VARCHAR(50) DEFAULT 'credit card' CHECK (
        method_type IN (
            'credit card',
            'cash',
            'paypal'
        )
    ),
    bank_name VARCHAR(255) NOT NULL DEFAULT 'N/A',
    users_id INTEGER NOT NULL,
    CONSTRAINT fk_users FOREIGN KEY (users_id) REFERENCES Users (id) ON DELETE CASCADE
);

CREATE TABLE Products (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    current_price NUMERIC(12, 2) NOT NULL,
    brand VARCHAR(255) NOT NULL,
    stock_code VARCHAR(50) UNIQUE,
    stock_quantity INTEGER DEFAULT 0,
    entry_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    
);

CREATE TABLE Invoices (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    type VARCHAR(32) CHECK (type IN ('SALE', 'CREDIT')) DEFAULT 'SALE',
    invoice_number INTEGER UNIQUE NOT NULL,
    total NUMERIC(12, 2) NOT NULL,
    status VARCHAR(32) CHECK (status IN ('ISSUED', 'CANCELLED', 'RETURNED')) DEFAULT 'ISSUED',
    purchase_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    payment_methods_id INTEGER NOT NULL,
    users_id INTEGER NOT NULL,
    CONSTRAINT fk_invoice_payment FOREIGN KEY (payment_methods_id) REFERENCES Payment_methods (id),
    CONSTRAINT fk_invoice_users FOREIGN KEY (users_id) REFERENCES Users (id)
);

CREATE TABLE Details (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    price_at_sale NUMERIC(12, 2) NOT NULL,
    quantity INTEGER DEFAULT 1,
    invoices_id INTEGER NOT NULL,
    products_id INTEGER NOT NULL,
    CONSTRAINT fk_details_invoice FOREIGN KEY (invoices_id) REFERENCES Invoices (id),
    CONSTRAINT fk_details_products FOREIGN KEY (products_id) REFERENCES Products (id)
);

CREATE TABLE Cart (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    users_id INTEGER NOT NULL,
    CONSTRAINT fk_cart_users FOREIGN KEY (users_id) REFERENCES Users (id) ON DELETE CASCADE
);

CREATE TABLE Cart_Products (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    cart_id INTEGER NOT NULL,
    products_id INTEGER NOT NULL,
    quantity INTEGER DEFAULT 1,
    CONSTRAINT fk_cp_cart FOREIGN KEY (cart_id) REFERENCES Cart (id) ON DELETE CASCADE,
    CONSTRAINT fk_cp_products FOREIGN KEY (products_id) REFERENCES Products (id) ON DELETE CASCADE
);
