
### Customers ###
| ID| Customer Name | Customer Phone |
| :--- | :--- | :--- |
| 001 | Alice | 123-456-7890 |
| 002 | Bob | 987-654-3210 | 
| 003 | Claire | 555-123-4567 |


### Addresses ###
| Id | Address | Customers_ID |
| :--- | :--- | :--- | 
| 001 | 123 Main St | 001 |
| 002 | 456 Elm St | 002 |
| 003 | 789 Oak St | 003 |
| 004 | 464 Georgia St | 003 |

*** 

### Orders ###

 | Id | Delivery Time | Addresses_Id |
 | :--- | :--- | :--- |
 | 001 | 6:00 PM | 001 |
 | 002 | 7:30 PM | 002 |
 | 003 | 12:00 PM | 003 |
 | 004 | 5:00 PM | 004 |

 ### Orders_Items ###
| Id | Order_Id | Item Id | Quantity | Special Request |
| :--- | :--- | :--- | :--- | :--- |
| 001 | 001 | 101 | 2 | No onions |
| 002 | 001 | 102 | 1 | Extra ketchup |
| 003 | 002 | 103 | 1 | Extra cheese |
| 004 | 002 | 104 | 2 | None |
| 005 | 003 | 105 | 1 | No croutons |
| 006 | 004 | 106 | 1 | None |


### Items ### 
| Id | Item Name | Price |
| :--- | :--- | :--- |
| 101 | Cheeseburger | $8 |
| 102 | Fries | $3 |
| 103 | Pizza | $12 |
| 104 | Salad | $6 |
| 105 | Water | $1 |
 


***
***
***

### Vehicles ###
| VIN | Models_ID | Year | Color |
| :--- | :--- | :--- | :--- |
| 1HGCM82633A | 001 | 2003 | Silver |
| 5J6RM4H79EL | 002 | 2014 | Blue |
| 1G1RA6EH1FU | 003 | 2015 | Red |

### Make ###
| ID | Make |
| :--- | :--- |
| 001 | Honda |
| 002 | Chevrolet |
 

### Models ###
| ID | Model | Make ID |
| :--- | :--- | :--- |
| 001 | Accord | 001 |
| 002 | CR-V | 001 |
| 003 | Volt | 002 |


### Vehicles_Owners ###
| VIN | Owner Id | Policy ID |
| :--- | :--- | :--- |
| 1HGCM82633A | 101 | 001|
| 1HGCM82633A | 102 | 002 |
| 5J6RM4H79EL | 103 | 003 |
| 1G1RA6EH1FU | 104 | 004 |

### Owners ###
| Id | Owner Name | Owner Phone |
| :--- | :--- | :--- |
| 101 | Alice | 123-456-7890 |
| 102 | Bob | 987-654-3210 |
| 103 | Claire | 555-123-4567 |
| 104 | Dave | 111-222-3333 |


### Policy ###
| Id | Policy Number | Insurance_Company_ID|
| :--- | :--- | :--- |
| 001  | POL12345 | 001 |
| 002  | POL54321 | 002 |
| 003  | POL67890 | 003 |
| 004  | POL98765 | 004 |

### Insurance Company ###
| Id | Insurance Company |
| :--- | :--- |
| 001 | ABC Insurance |
| 002 | XYZ Insurance |
| 003 | DEF Insurance |
| 004 | GHI Insurance |

