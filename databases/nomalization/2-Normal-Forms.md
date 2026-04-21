================================================================================
Employees and Projects
================================================================================
Emp ID | Name        | Department | Dept Phone | Proj ID | Project Name | Budget
-------|-------------|------------|------------|---------|--------------|-------
201    | Ana Rivera  | IT         | 2222-2222  | P001    | Web App      | 50000
201    | Ana Rivera  | IT         | 2222-2222  | P002    | API REST     | 25000
202    | Luis Mendez | Marketing  | 1111-1111  | P003    | Campaña TV   | 30000

This table is already in `1NF`, no repeating groups and fields are atomic. 
For `2NF` we see functional dependencies, we see several related entities in the table
We will move the columns to fields that depend only on the key to have it in `2NF`. 
(Assuming the Primary Key is composite (Emp ID, Proj ID))

### Employees ###
| Id | Name          | Department | Dept Phone |
|------|-------------|------------|------------|
| 201  | Ana Rivera  | IT         | 2222-2222  |
| 202  | Luis Mendez | Marketing  | 1111-1111  |

### Employee Projects ###
| Employee_Id | Project_Id |          
|-------------|------------|
| 201         | P001       |
| 201         | P002       |
| 202         | P003       |

### Projects ###
| Id      | Project Name | Budget |
|---------|--------------|--------|
| P001    | Web App      | 50000  |
| P002    | API REST     | 25000  |
| P003    | Campaña TV   | 30000  |

We change the data to `3NF` by eliminating transitive dependencies.

### Employees ###
| Id   | Name        | Departments_Id |
|------|-------------|----------------|
| 201  | Ana Rivera  |     001        |
| 202  | Luis Mendez |     002        |      


### Departments ###
| Id  | Department | Dept Phone |
|-----|------------|------------|
| 001 |    IT      | 2222-2222  |
| 002 | Marketing  | 1111-1111  | 


### Employee Projects ###
| Employee_Id | Project_Id |          
|-------------|------------|
| 201         | P001       |
| 201         | P002       |
| 202         | P003       |

### Projects ###
| Id      | Project Name | Budget |
|---------|--------------|--------|
| P001    | Web App      | 50000  |
| P002    | API REST     | 25000  |
| P003    | Campaña TV   | 30000  |


================================================================================
Class Registry
================================================================================
Stu ID | Student Name | Code  | Course Name | Instructor   | Instructor Email
-------|--------------|-------|-------------|--------------|-----------------
301    | Marco Gómez  | CS101 | Python I    | Juan Pérez   | juan@uni.edu
301    | Marco Gómez  | CS102 | Python II   | Laura Rojas  | laura@uni.edu
302    | Carla Ruiz   | CS101 | Python I    | Juan Pérez   | juan@uni.edu

This table is already in `1NF`, no repeating groups and fields are atomic.
For `2NF`we can take `( STU ID, Code )`


### Students ###
Stu ID | Student Name | 
-------|--------------|
301    | Marco Gómez  |
302    | Carla Ruiz   |


### Enrollments ###
Stu ID | Code   |
-------|--------|
  301  |  CS101 |
  301  |  CS102 |
  302  |  CS101 |


### Courses ###
Code   | Course Name | Instructor   | Instructor Email
-------|------------|---------------|-----------------
 CS101 | Python I    | Juan Pérez   | juan@uni.edu
 CS102 | Python II   | Laura Rojas  | laura@uni.edu

Finally to move to `3NF`, we can split the `Courses` table into Courses and Instructors

### Students ###
Stu ID | Student Name | 
-------|--------------|
301    | Marco Gómez  |
302    | Carla Ruiz   |


### Enrollments ###
|Stu ID | Code   |
|-------|--------|
|  301  |  CS101 |
|  301  |  CS102 |
|  302  |  CS101 |


### Courses ###
|Code   | Course Name | Instructors_ID |
|-------|-------------|----------------|
| CS101 | Python I    |    1001        |
| CS102 | Python II   |    1002        |


### Instructors ###
| ID   | Instructor   | Instructor Email |
|------|--------------|------------------|
| 1001 |  Juan Pérez  | juan@uni.edu     |
| 1002 |  Laura Rojas  | laura@uni.edu   |


================================================================================
Hospitals and Medical Appointments
================================================================================
Appt ID| Patient Name | Phone     | Doctor Name | Specialty   | Date/Time
-------|--------------|-----------|-------------|-------------|------------------
A01    | Diana Vargas | 8888-1111 | Dr. Soto    | Pediatría   | 2024-08-01 10:00AM
A02    | Diana Vargas | 8888-1111 | Dr. Soto    | Pediatría   | 2024-08-10 10:00AM
A03    | Edwin Mora   | 8999-2222 | Dr. Mora    | Cardiología | 2024-08-05 01:00PM


We update this table to `1NF`, no repeating groups and fields are atomic. 
This table is already in `2NF`, not partial dependencies on the primary key that by definition can
just happen for composite keys.

Appt ID| Patient Name | Phone     | Doctor Name | Specialty   | Date          |  Time     |
-------|--------------|-----------|-------------|-------------|---------------|-----------|
A01    | Diana Vargas | 8888-1111 | Dr. Soto    | Pediatría   | 2024-08-01    | 10:00AM   |
A02    | Diana Vargas | 8888-1111 | Dr. Soto    | Pediatría   | 2024-08-10    | 10:00AM   |
A03    | Edwin Mora   | 8999-2222 | Dr. Mora    | Cardiología | 2024-08-05    | 01:00PM   |


Now we need to change the table to `3NF` by eliminating transitive dependencies. Patient and doctor
depend dont' depend directly on the Appt ID.

### Appointments ###
| Appt ID |Patients_ID | Doctors_ID  |     Date    |  Time     |
|---------|------------|-------------|-------------|-----------|
|   A01   | P001       | D001        | 2024-08-01  |  10:00AM  |
|   A02   | P001       | D001        | 2024-08-10  |  10:00AM  |
|   A03   | P002       | D002        | 2024-08-05  |  01:00PM  |


### Patients ###
| ID   | Patient Name  | Phone      |
|------|---------------|------------|
| P001 | Diana Vargas  | 8888-1111  |
| P002 | Edwin Mora    | 8999-2222  |


### Doctors ###
| ID   | Doctor Name | Specialty   |
|------|-------------|-------------|
| D001 | Dr. Soto    | Pediatría   |
| D002 | Dr. Mora    | Cardiología | 

