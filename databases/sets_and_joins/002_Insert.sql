INSERT INTO Authors (ID, Name) VALUES 
(1, 'Miguel de Cervantes'),
(2, 'Dante Alighieri'),
(3, 'Takehiko Inoue'),
(4, 'Akira Toriyama'),
(5, 'Walt Disney');


INSERT INTO Books (ID, Name, Author) VALUES 
(1, 'Don Quijote', 1),
(2, 'La Divina Comedia', 2),
(3, 'Vagabond 1-3', 3),
(4, 'Dragon Ball 1', 4),
(5, 'The Book of the 5 Rings', NULL);

INSERT INTO Customers (ID, Name, Email) VALUES 
(1, 'John Doe', 'j.doe@email.com'),
(2, 'Jane Doe', 'jane@doe.com'),
(3, 'Luke Skywalker', 'darth.son@email.com');

INSERT INTO Rents (ID, State, Books_ID, Customers_ID ) VALUES
(1, 'Returned', 1, 2),
(2, 'Returned', 2, 2),
(3, 'On time', 1, 1),
(4, 'On time', 3, 1),
(5, 'Overdue', 2, 2);
