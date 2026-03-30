PRAGMA foreign_keys = ON;

CREATE TABLE Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL CHECK (length(full_name) <= 255),
    email TEXT UNIQUE NOT NULL CHECK (length(email) <= 255),
    registration_day DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Payment_methods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    method_type TEXT DEFAULT 'Pending' CHECK (method_type IN ('credit card', 'cash', 'paypal')),
    bank_name TEXT NOT NULL CHECK (length(bank_name) <= 255),
    users_id INTEGER NOT NULL,
    FOREIGN KEY (users_id) REFERENCES Users(id)    
);

CREATE TABLE Products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL CHECK (length(name) <= 255),
    current_price REAL NOT NULL,
    entry_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    brand TEXT NOT NULL CHECK (length(brand) <= 255),
    sku INTEGER DEFAULT 0
);

CREATE TABLE Invoices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_number INTEGER NOT NULL,
    purchase_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    total REAL NOT NULL,
    payment_methods_id INTEGER NOT NULL,
    users_id INTEGER NOT NULL,
    FOREIGN KEY (payment_methods_id) REFERENCES Payment_methods(id),
    FOREIGN KEY (users_id) REFERENCES Users(id)
);


CREATE TABLE Details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    price_at_sale REAL NOT NULL,
    quantity INTEGER DEFAULT 0,
    invoices_id INTEGER NOT NULL,
    products_id INTEGER NOT NULL,
    FOREIGN KEY (invoices_id) REFERENCES Invoices(id),
    FOREIGN KEY (products_id) REFERENCES Products(id)
);


CREATE TABLE Cart (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    users_id INTEGER NOT NULL,
    FOREIGN KEY (users_id) REFERENCES Users(id)    
);

CREATE TABLE Cart_Products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cart_id INTEGER NOT NULL,
    products_id INTEGER NOT NULL,
    FOREIGN KEY (cart_id) REFERENCES Cart(id),
    FOREIGN KEY (products_id) REFERENCES Products(id)
);

CREATE TABLE Reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    comment TEXT,
    rating INTEGER CHECK (rating BETWEEN 1 AND 5),
    date DATETIME DEFAULT CURRENT_TIMESTAMP,
    users_id INTEGER NOT NULL,
    products_id INTEGER NOT NULL,
    FOREIGN KEY (users_id) REFERENCES Users(id),
    FOREIGN KEY (products_id) REFERENCES Products(id)   
);

