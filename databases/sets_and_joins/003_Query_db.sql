-- 1) Get all Books and its Authors

SELECT Books.ID, Books.name,  Authors.name AS Author_name
FROM Books
LEFT JOIN Authors ON Books.Author = Authors.ID;

-- | ID | name | Author_name |
-- | :--- | :--- | :--- |
-- | 1 | Don Quijote | Miguel de Cervantes |
-- | 2 | La Divina Comedia | Dante Alighieri |
-- | 3 | Vagabond 1-3 | Takehiko Inoue |
-- | 4 | Dragon Ball 1 | Akira Toriyama |
-- | 5 | The Book of the 5 Rings | NULL |

-- 2) Get all the Books that have no Author
SELECT ID, name FROM Books
WHERE Author IS NULL;

-- | ID | name                    |
-- |----|-------------------------|
-- |  5 | The Book of the 5 Rings |


-- 3) Get all Authors that have no Books
SELECT Authors.ID, Authors.name
FROM Books
RIGHT JOIN Authors ON Books.Author = Authors.ID
Where Books.ID IS NULL;

-- | ID | name        |
-- |----|-------------|
-- |  5 | Walt Disney |

-- 4) Get all the books that have been rented at least once
Select Books.ID, Books.name  FROM Rents
RIGHT JOIN Books ON Books.ID = Rents.Books_ID
WHERE Rents.Customers_ID IS NOT NULL
GROUP BY Books.ID;

| ID   |        name       |
| :--- | :-----------------|
| 1    | Don Quijote       |
| 2    | La Divina Comedia |
| 3    | Vagabond 1-3      |


-- 5) Get all the books that have never been rented
Select Books.ID, Books.name FROM Rents
RIGHT JOIN Books ON Books.ID = Rents.Books_ID
WHERE Rents.Customers_ID IS NULL
GROUP BY Books.ID;

| ID   |        name             |
| :--- | :-----------------------|
| 4    | Dragon Ball 1           |
| 5    | The Book of the 5 Rings |
        
-- 6) Get all the clients that have never rented a book
Select Customers.ID, Customers.name, Customers.email FROM Customers
LEFT JOIN Rents ON Customers.ID = Rents.Customers_ID
WHERE Rents.Customers_ID IS NULL;

| ID   | name           | email               |
| :--- | :------------- | :------------------ |
| 3    | Luke Skywalker | darth.son@email.com |

-- 7)  Get all the books that have been rented and are in "Overdue" state.
Select Books.ID, Books.name FROM Books
INNER JOIN Rents ON Books.ID = Rents.Books_ID
WHERE Rents.State = "Overdue";

| ID   | name              |
| :--- | :---------------- |
| 2    | La Divina Comedia |
