
# 1 #

The tables start in first normal form (`1NF`).

| Order ID | Customer Name | Customer Phone | Address | Item ID | Item Name | Price | Quantity | Special Request | Delivery Time |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 001 | Alice | 123-456-7890 | 123 Main St | 101 | Cheeseburger | $8 | 2 | No onions | 6:00 PM |
| 001 | Alice | 123-456-7890 | 123 Main St | 102 | Fries | $3 | 1 | Extra ketchup | 6:00 PM |
| 002 | Bob | 987-654-3210 | 456 Elm St | 103 | Pizza | $12 | 1 | Extra cheese | 7:30 PM |
| 002 | Bob | 987-654-3210 | 456 Elm St | 104 | Fries | $3 | 2 | None | 7:30 PM |
| 003 | Claire | 555-123-4567 | 789 Oak St | 105 | Salad | $6 | 1 | No croutons | 12:00 PM |
| 004 | Claire | 555-123-4567 | 464 Georgia St | 106 | Water | $1 | 1 | None | 5:00 PM |


***
No single column identifies, the primary key, there are several partial dependencies violating 2NF,
therefore we can start by splitting in a somewhat natural way, Orders and Customers are two separate concepts
which looks like a good starting point.

## Orders ##

| Order ID | Item ID | Item Name | Price | Quantity | Special Request | Delivery Time |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 001| 101 | Cheeseburger | $8 | 2 | No onions | 6:00 PM |
| 001 | 102 | Fries | $3 | 1 | Extra ketchup | 6:00 PM |
| 002 | 103 | Pizza | $12 | 1 | Extra cheese | 7:30 PM |
| 002 | 104 | Fries | $3 | 2 | None | 7:30 PM |
| 003 | 105 | Salad | $6 | 1 | No croutons | 12:00 PM |
| 004 | 106 | Water | $1 | 1 | None | 5:00 PM |


## Customers ##

| Customer ID| Customer Name | Customer Phone | Address |
| :--- | :--- | :--- | :--- |
| 001 | Alice | 123-456-7890 | 123 Main St |
| 002 | Alice | 123-456-7890 | 123 Main St |
| 003 | Bob | 987-654-3210 | 456 Elm St |
| 004 | Claire | 555-123-4567 | 789 Oak St |
| 005 | Claire | 555-123-4567 | 464 Georgia St |

***

Let's start with the data on the customer side.

| Customer ID| Customer Name | Customer Phone | Address |
| :--- | :--- | :--- | :--- |
| 001 | Alice | 123-456-7890 | 123 Main St |
| 002 | Alice | 123-456-7890 | 123 Main St |
| 003 | Bob | 987-654-3210 | 456 Elm St |
| 004 | Claire | 555-123-4567 | 789 Oak St |
| 005 | Claire | 555-123-4567 | 464 Georgia St |

We normalize the table to `Customers` and `Addresess` plus an intermediate cross table `Customer_Addresses`
which expresses a relation many to many. We are done on the `Customers` side of the tables. 

As a side note, this normalization form is the 4NF or 5NF which is outside of the course scope. But we can intuitively see duplication
can lead to an anomaly in the data and identify the entities that have a many to many relationship Addresses and Customers.

### Customers ###
| Customer ID| Customer Name | Customer Phone |
| :--- | :--- | :--- |
| 001 | Alice | 123-456-7890 |
| 002 | Bob | 987-654-3210 | 
| 003 | Claire | 555-123-4567 |

### Customer_Addresses ###
| Customer ID| Address ID |
| :--- | :--- | 
|001 | 001 |
|002 | 002 |
|003 | 003 |
|003 | 004 |

### Addresses ###
| Address ID | Address
| :--- | :--- |
| 001 | 123 Main St |
| 002 | 456 Elm St |
| 003 | 789 Oak St |
| 004 | 464 Georgia St |

With that done, let's move to the orders side:

*** 

## Orders ##

| Order ID | Item ID | Item Name | Price | Quantity | Special Request | Delivery Time |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 001| 101 | Cheeseburger | $8 | 2 | No onions | 6:00 PM |
| 001 | 102 | Fries | $3 | 1 | Extra ketchup | 6:00 PM |
| 002 | 103 | Pizza | $12 | 1 | Extra cheese | 7:30 PM |
| 002 | 104 | Fries | $3 | 2 | None | 7:30 PM |
| 003 | 105 | Salad | $6 | 1 | No croutons | 12:00 PM |
| 004 | 106 | Water | $1 | 1 | None | 5:00 PM |

No single key in this table is the primary key, we can use (`Order ID`, `Item ID`), there are partial dependencies that violate the `2NF`
we can think that a natural concept is `Orders`, let's start by taking an attribute that relates only to `Order ID` which is the `Delivery Time`. It hardly relates to anything else, and other concepts are just transitively dependent on the order so we leave it as a rather simple table.

### Orders ###

 Order ID | Delivery Time |
 | :--- | :--- | 
 | 001 | 6:00 PM |
 | 002 | 7:30 PM |
 | 003 | 12:00 PM |
 | 004 | 5:00 PM |

`Items` is also a natural concept, we can create the table taking just the concepts that are part of it
and not in the relation between Items and Orders, an Item has a name and I assign a price to a specific item.

Items
| Item ID | Item Name | Price |
| :--- | :--- | :--- |
| 101 | Cheeseburger | $8 |
| 102 | Fries | $3 |
| 103 | Pizza | $12 |
| 104 | Fries | $3 |
| 105 | Salad | $6 |
| 106 | Water | $1 |
 
Finally we see a relationship many to many between Items and Orders
and the attributes of that relationship

### Orders_Items ###
| Order ID | Item ID | Quantity | Special Request |
| :--- | :--- | :--- | :--- |
| 001| 101 | 2 | No onions |
| 001 | 102 | 1 | Extra ketchup |
| 002 | 103 | 1 | Extra cheese |
| 002 | 104 | 2 | None |
| 003 | 105 | 1 | No croutons |
| 004 | 106 | 1 | None |

***

# 2 #
### Vehicles ###
| VIN | Make | Model | Year | Color | Owner ID | Owner Name | Owner Phone | Insurance Company | Insurance Policy |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1HGCM82633A | Honda | Accord | 2003 | Silver | 101 | Alice | 123-456-7890 | ABC Insurance | POL12345 |
| 1HGCM82633A | Honda | Accord | 2003 | Silver | 102 | Bob | 987-654-3210 | XYZ Insurance | POL54321 |
| 5J6RM4H79EL | Honda | CR-V | 2014 | Blue | 103 | Claire | 555-123-4567 | DEF Insurance | POL67890 |
| 1G1RA6EH1FU | Chevrolet | Volt | 2015 | Red | 104 | Dave | 111-222-3333 | GHI Insurance | POL98765 |



We can take a composite primary key: (VIN, Owner ID), from there:
This table violates 2NF because of the dependency of the attributes to other non primary key values or partial key dependency
it also breaks 3NF because of transitive dependency:
    ```
    Insurance Policy → Insurance Company
    ```
## Normalized Tables
 
Vehicle is a natural concept in the table, we can make a table for it and its own attributes.

### Vehicles ###
| VIN | Make | Model | Year | Color |
| :--- | :--- | :--- | :--- | :--- |
| 1HGCM82633A | Honda | Accord | 2003 | Silver |
| 5J6RM4H79EL | Honda | CR-V | 2014 | Blue |
| 1G1RA6EH1FU | Chevrolet | Volt | 2015 | Red |
 
The same way for Onwers and it's attribute, they are grouped in the bigger Vehicles table
### Owners ###
| Owner ID | Owner Name | Owner Phone |
| :--- | :--- | :--- |
| 101 | Alice | 123-456-7890 |
| 102 | Bob | 987-654-3210 |
| 103 | Claire | 555-123-4567 |
| 104 | Dave | 111-222-3333 |
 
From the bigger table we can a many to many relationship between `Vehicles` and `Owners`
### Vehicles_Owners ###
| VIN | Owner ID | Policy Number |
| :--- | :--- | :--- |
| 1HGCM82633A | 101 | POL12345 |
| 1HGCM82633A | 102 | POL54321 |
| 5J6RM4H79EL | 103 | POL67890 |
| 1G1RA6EH1FU | 104 | POL98765 |
 
And last but not least Insurance is it's own entity.
### Insurance ###
| Policy Number | Insurance Company |
| :--- | :--- |
| POL12345 | ABC Insurance |
| POL54321 | XYZ Insurance |
| POL67890 | DEF Insurance |
| POL98765 | GHI Insurance |
 
