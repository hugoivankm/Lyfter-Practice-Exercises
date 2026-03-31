ALTER TABLE Users
ADD COLUMN phone_number TEXT CHECK (length(phone_number) <= 25);

ALTER TABLE Invoices
ADD COLUMN employee_number INTEGER;
