#!/usr/bin/env python3
"""
Replace ALL code blocks in all 14 HTML files with clean, plain-escaped SQL.
Removes the broken nested-span syntax highlighting and uses just JetBrains Mono
on the dark bg-[#0a0e14] background which looks perfectly readable.
"""

import html, os, re

BASE = os.path.dirname(os.path.abspath(__file__))

# ─── Plain SQL code for every practical ───────────────────────────────────────

CODES = {

"practical_01_study_of_mysql": (
"MySQL 8.x — System Exploration Queries",
"""-- ============================================================
-- Practical 01: Study of MySQL — Exploration Queries
-- S.Y.B.Tech IT | Sem IV | Subject: 2308215
-- ============================================================

-- Step 1: Display the current MySQL version
SELECT VERSION() AS MySQL_Version;

-- Step 2: Display currently logged-in user
SELECT USER() AS Current_User;

-- Step 3: Display current date and time
SELECT NOW() AS Current_DateTime;

-- Step 4: Show ALL databases on this server
SHOW DATABASES;

-- Step 5: Show ALL available storage engines
SHOW ENGINES;

-- Step 6: Show version-related system variables
SHOW VARIABLES LIKE 'version%';

-- Step 7: Show the default storage engine
SHOW VARIABLES LIKE '%default_storage_engine%';

-- Step 8: Show maximum allowed connections
SHOW VARIABLES LIKE 'max_connections';

-- Step 9: Show default character set
SHOW VARIABLES LIKE 'character_set_database';

-- Step 10: Show the port MySQL is running on
SHOW VARIABLES LIKE 'port';

-- Step 11: Show InnoDB buffer pool size
SHOW VARIABLES LIKE 'innodb_buffer_pool_size';

-- Step 12: Create a new database for lab practicals
CREATE DATABASE IF NOT EXISTS dbms_lab
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

-- Step 13: Switch to the new database
USE dbms_lab;

-- Step 14: Confirm which database is currently active
SELECT DATABASE() AS Active_DB;

-- Step 15: Show all tables (empty initially)
SHOW TABLES;

-- Step 16: Show server uptime and connection stats
SHOW STATUS LIKE 'Uptime';
SHOW STATUS LIKE 'Connections';
SHOW STATUS LIKE 'Questions';

-- Step 17: Show grants for root user
SHOW GRANTS FOR 'root'@'localhost';

-- Step 18: Full server status summary
STATUS;"""),

"practical_02_mysql_installation": (
"MySQL 8.x — Installation, Configuration & User Management",
"""-- ============================================================
-- Practical 02: MySQL Installation & Configuration
-- S.Y.B.Tech IT | Sem IV | Subject: 2308215
-- ============================================================

-- Step 1: Connect to MySQL as root (run in terminal)
-- mysql -u root -p

-- Step 2: Check current MySQL version
SELECT VERSION() AS MySQL_Version;

-- Step 3: View all existing users and their allowed hosts
SELECT User, Host, plugin FROM mysql.user;

-- Step 4: Create a new database for lab work
CREATE DATABASE IF NOT EXISTS dbms_lab
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

-- Step 5: Create a new database user for lab work
CREATE USER 'labuser'@'localhost' IDENTIFIED BY 'Lab@1234';

-- Step 6: Grant all privileges on the lab database
GRANT ALL PRIVILEGES ON dbms_lab.* TO 'labuser'@'localhost';

-- Step 7: Apply the privilege changes immediately
FLUSH PRIVILEGES;

-- Step 8: Verify what privileges were granted
SHOW GRANTS FOR 'labuser'@'localhost';

-- Step 9: Create a read-only restricted user
CREATE USER 'readonly_user'@'localhost' IDENTIFIED BY 'Read@5678';
GRANT SELECT ON dbms_lab.* TO 'readonly_user'@'localhost';
FLUSH PRIVILEGES;

-- Step 10: Show grants for restricted user
SHOW GRANTS FOR 'readonly_user'@'localhost';

-- Step 11: Revoke INSERT privilege from labuser
REVOKE INSERT ON dbms_lab.* FROM 'labuser'@'localhost';

-- Step 12: Check important configuration variables
SHOW VARIABLES LIKE 'max_connections';
SHOW VARIABLES LIKE 'character_set_server';
SHOW VARIABLES LIKE 'collation_server';
SHOW VARIABLES LIKE 'innodb_buffer_pool_size';
SHOW VARIABLES LIKE 'datadir';
SHOW VARIABLES LIKE 'log_error';
SHOW VARIABLES LIKE 'port';

-- Step 13: Change session-level character set
SET NAMES 'utf8mb4';

-- Step 14: Verify session character set
SHOW VARIABLES LIKE 'character_set_client';

-- Step 15: Drop test users (cleanup)
DROP USER IF EXISTS 'readonly_user'@'localhost';
DROP USER IF EXISTS 'labuser'@'localhost';

-- Step 16: Verify users were dropped
SELECT User, Host FROM mysql.user WHERE User NOT IN ('root','mysql.sys','mysql.infoschema');"""),

"practical_03_sqlite_study": (
"SQLite3 — College Student Database",
"""-- ============================================================
-- Practical 03: Study of SQLite
-- S.Y.B.Tech IT | Sem IV | Subject: 2308215
-- Run these commands in: sqlite3 college.db
-- ============================================================

-- Step 1: Open or create a SQLite database file
.open college.db

-- Step 2: Show all attached databases
.databases

-- Step 3: Enable column headers and formatted output
.headers on
.mode column

-- Step 4: Create the Students table
CREATE TABLE IF NOT EXISTS Students (
    StudentID  INTEGER PRIMARY KEY AUTOINCREMENT,
    Name       TEXT    NOT NULL,
    Branch     TEXT    NOT NULL,
    Semester   INTEGER CHECK(Semester BETWEEN 1 AND 8),
    CGPA       REAL    DEFAULT 0.0 CHECK(CGPA BETWEEN 0.0 AND 10.0),
    Email      TEXT    UNIQUE
);

-- Step 5: Insert 15 rows of sample student data
INSERT INTO Students (Name, Branch, Semester, CGPA, Email) VALUES
('Aarav Shah',    'IT',    4, 8.5, 'aarav@college.edu'),
('Priya Mehta',   'CS',    4, 9.1, 'priya@college.edu'),
('Rohit Joshi',   'ENTC',  4, 7.8, 'rohit@college.edu'),
('Sneha Patil',   'IT',    4, 8.9, 'sneha@college.edu'),
('Karan Desai',   'Mech',  4, 6.5, 'karan@college.edu'),
('Ananya Iyer',   'CS',    4, 9.4, 'ananya@college.edu'),
('Vikas Rao',     'Civil', 4, 7.2, 'vikas@college.edu'),
('Pooja Nair',    'IT',    4, 8.0, 'pooja@college.edu'),
('Arjun Tiwari',  'CS',    4, 8.7, 'arjun@college.edu'),
('Neha Gupta',    'ENTC',  4, 7.5, 'neha@college.edu'),
('Raj Malhotra',  'IT',    4, 9.0, 'raj@college.edu'),
('Meera Pillai',  'Mech',  4, 6.8, 'meera@college.edu'),
('Dev Sharma',    'CS',    4, 8.3, 'dev@college.edu'),
('Tara Jain',     'IT',    4, 7.9, 'tara@college.edu'),
('Yash Kumar',    'ENTC',  4, 8.1, 'yash@college.edu');

-- Step 6: Select all students
SELECT * FROM Students;

-- Step 7: Filter IT branch students
SELECT Name, CGPA FROM Students WHERE Branch = 'IT';

-- Step 8: Order by CGPA descending
SELECT Name, Branch, CGPA FROM Students ORDER BY CGPA DESC;

-- Step 9: Count students per branch with average CGPA
SELECT Branch,
       COUNT(*)   AS TotalStudents,
       AVG(CGPA)  AS AvgCGPA
FROM Students
GROUP BY Branch;

-- Step 10: Students with CGPA above 8.5
SELECT Name, Branch, CGPA FROM Students WHERE CGPA > 8.5;

-- Step 11: Show table schema
.schema Students

-- Step 12: Export results to a file
.output students_report.txt
SELECT * FROM Students ORDER BY CGPA DESC;
.output stdout

-- Step 13: Show column metadata using PRAGMA
PRAGMA table_info(Students);

-- Step 14: Count total students
SELECT COUNT(*) AS TotalStudents FROM Students;

-- Step 15: Drop the table and exit
DROP TABLE IF EXISTS Students;
.quit"""),

"practical_04_er_diagrams": (
"MySQL 8.x — Hospital Management System (ER Diagram Implementation)",
"""-- ============================================================
-- Practical 04: ER Diagrams
-- Case Study: Hospital Management System
-- S.Y.B.Tech IT | Sem IV | Subject: 2308215
-- ============================================================

CREATE DATABASE IF NOT EXISTS hospital_db;
USE hospital_db;

-- Strong Entity: Doctor
CREATE TABLE Doctor (
    DoctorID       INT PRIMARY KEY AUTO_INCREMENT,
    Name           VARCHAR(100) NOT NULL,
    Specialization VARCHAR(50)  NOT NULL,
    Phone          VARCHAR(15)  UNIQUE,
    Email          VARCHAR(100) UNIQUE,
    JoiningDate    DATE         DEFAULT (CURRENT_DATE)
);

-- Strong Entity: Ward
CREATE TABLE Ward (
    WardID   INT PRIMARY KEY AUTO_INCREMENT,
    WardName VARCHAR(50)  NOT NULL,
    WardType ENUM('General','ICU','Pediatric','Emergency') NOT NULL,
    Capacity INT          CHECK (Capacity > 0),
    Floor    INT          DEFAULT 1
);

-- Strong Entity: Patient  (linked to Ward via 1:N relationship)
CREATE TABLE Patient (
    PatientID INT PRIMARY KEY AUTO_INCREMENT,
    Name      VARCHAR(100) NOT NULL,
    Age       INT          CHECK (Age > 0 AND Age < 150),
    Gender    ENUM('Male','Female','Other') NOT NULL,
    Phone     VARCHAR(15),
    Address   TEXT,
    WardID    INT,
    FOREIGN KEY (WardID) REFERENCES Ward(WardID)
);

-- M:N Relationship Table: Treatment  (Patient ↔ Doctor)
CREATE TABLE Treatment (
    TreatmentID   INT PRIMARY KEY AUTO_INCREMENT,
    PatientID     INT          NOT NULL,
    DoctorID      INT          NOT NULL,
    TreatmentDate DATE         NOT NULL,
    Diagnosis     VARCHAR(200),
    Prescription  TEXT,
    Cost          DECIMAL(8,2) DEFAULT 0.00,
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID),
    FOREIGN KEY (DoctorID)  REFERENCES Doctor(DoctorID)
);

-- Insert 5 Doctors
INSERT INTO Doctor (Name, Specialization, Phone, Email) VALUES
('Dr. Anil Kapoor',  'Cardiology',   '9876543210', 'anil@hospital.com'),
('Dr. Sunita Rao',   'Neurology',    '9876543211', 'sunita@hospital.com'),
('Dr. Rajan Mehta',  'Orthopedics',  '9876543212', 'rajan@hospital.com'),
('Dr. Priya Sharma', 'Pediatrics',   '9876543213', 'priya@hospital.com'),
('Dr. Vikram Singh', 'Emergency',    '9876543214', 'vikram@hospital.com');

-- Insert 5 Wards
INSERT INTO Ward (WardName, WardType, Capacity, Floor) VALUES
('Ward A', 'General',   50, 1),
('Ward B', 'ICU',       10, 2),
('Ward C', 'Pediatric', 20, 3),
('Ward D', 'Emergency', 15, 1),
('Ward E', 'General',   40, 2);

-- Insert 10 Patients
INSERT INTO Patient (Name, Age, Gender, Phone, WardID) VALUES
('Ramesh Kumar',  45, 'Male',   '9111111111', 1),
('Sunita Devi',   32, 'Female', '9222222222', 3),
('Aakash Singh',  67, 'Male',   '9333333333', 2),
('Priya Verma',   28, 'Female', '9444444444', 1),
('Vijay Patil',   55, 'Male',   '9555555555', 2),
('Meena Shah',     8, 'Female', '9666666666', 3),
('Rajesh Gupta',  72, 'Male',   '9777777777', 2),
('Anita Joshi',   41, 'Female', '9888888888', 4),
('Suresh Nair',   35, 'Male',   '9999999999', 1),
('Kavita Pillai', 60, 'Female', '9000000001', 5);

-- Insert 10 Treatment records  (M:N Patient-Doctor relationship)
INSERT INTO Treatment (PatientID, DoctorID, TreatmentDate, Diagnosis, Cost) VALUES
(1, 1, '2024-01-10', 'Hypertension',    2500.00),
(2, 2, '2024-01-11', 'Migraine',        1800.00),
(3, 1, '2024-01-12', 'Bypass Surgery', 85000.00),
(4, 3, '2024-01-13', 'Knee Replacement',65000.00),
(5, 2, '2024-01-14', 'Stroke',         45000.00),
(6, 4, '2024-01-15', 'Fever',            500.00),
(7, 1, '2024-01-16', 'Heart Attack',   90000.00),
(8, 5, '2024-01-17', 'Fracture',       12000.00),
(9, 3, '2024-01-18', 'Back Pain',       3500.00),
(10,4, '2024-01-19', 'Diabetes',        2000.00);

-- Query 1: Patient with their Ward (1:N)
SELECT P.Name AS Patient, W.WardName, W.WardType
FROM Patient P
JOIN Ward W ON P.WardID = W.WardID;

-- Query 2: Full treatment view (M:N)
SELECT P.Name AS Patient, D.Name AS Doctor,
       D.Specialization, T.Diagnosis, T.Cost
FROM Treatment T
JOIN Patient P ON T.PatientID = P.PatientID
JOIN Doctor  D ON T.DoctorID  = D.DoctorID
ORDER BY T.TreatmentDate;

-- Query 3: Doctor revenue summary
SELECT D.Name, COUNT(T.PatientID) AS Patients,
       SUM(T.Cost) AS TotalRevenue
FROM Doctor D
LEFT JOIN Treatment T ON D.DoctorID = T.DoctorID
GROUP BY D.DoctorID
ORDER BY TotalRevenue DESC;"""),

"practical_05_ddl_normalization": (
"MySQL 8.x — DDL Commands & Normalization (UNF → 1NF → 2NF → 3NF)",
"""-- ============================================================
-- Practical 05: DDL Commands & Normalization
-- S.Y.B.Tech IT | Sem IV | Subject: 2308215
-- ============================================================

CREATE DATABASE IF NOT EXISTS college_db;
USE college_db;

-- ── UNNORMALIZED (UNF) ──
-- Courses column holds multiple values in ONE cell => violates 1NF
CREATE TABLE UNF_StudentCourses (
    StudentID      INT,
    StudentName    VARCHAR(100),
    Courses        VARCHAR(500),   -- 'DBMS, OS, CN' in one cell
    ProfessorNames VARCHAR(500),
    Department     VARCHAR(50)
);

-- ── 1NF: Atomic values, composite primary key ──
CREATE TABLE NF1_StudentCourses (
    StudentID    INT,
    StudentName  VARCHAR(100),
    CourseID     VARCHAR(10),
    CourseName   VARCHAR(100),
    ProfessorName VARCHAR(100),
    Department   VARCHAR(50),
    PRIMARY KEY (StudentID, CourseID)
);

-- ── 2NF: Remove partial dependencies ──
-- StudentName/Department depend only on StudentID (partial dep)
-- CourseName/ProfessorName depend only on CourseID (partial dep)
CREATE TABLE NF2_Students (
    StudentID   INT PRIMARY KEY,
    StudentName VARCHAR(100) NOT NULL,
    Department  VARCHAR(50)
);

CREATE TABLE NF2_Courses (
    CourseID      VARCHAR(10) PRIMARY KEY,
    CourseName    VARCHAR(100) NOT NULL,
    ProfessorName VARCHAR(100),
    ProfessorDept VARCHAR(50)   -- transitive dep (will fix in 3NF)
);

CREATE TABLE NF2_Enrollment (
    StudentID   INT,
    CourseID    VARCHAR(10),
    EnrollDate  DATE DEFAULT (CURRENT_DATE),
    PRIMARY KEY (StudentID, CourseID),
    FOREIGN KEY (StudentID) REFERENCES NF2_Students(StudentID),
    FOREIGN KEY (CourseID)  REFERENCES NF2_Courses(CourseID)
);

-- ── 3NF: Remove transitive dependency ──
-- ProfessorDept depends on ProfessorName, not on CourseID
CREATE TABLE NF3_Professors (
    ProfessorID   INT PRIMARY KEY AUTO_INCREMENT,
    ProfessorName VARCHAR(100) NOT NULL,
    Department    VARCHAR(50)  NOT NULL,
    Email         VARCHAR(100) UNIQUE
);

CREATE TABLE NF3_Courses (
    CourseID    VARCHAR(10) PRIMARY KEY,
    CourseName  VARCHAR(100) NOT NULL,
    Credits     INT DEFAULT 3,
    ProfessorID INT,
    FOREIGN KEY (ProfessorID) REFERENCES NF3_Professors(ProfessorID)
);

-- Insert 15 students
INSERT INTO NF2_Students VALUES
(1,'Aarav Shah','IT'),(2,'Priya Mehta','CS'),(3,'Rohit Joshi','ENTC'),
(4,'Sneha Patil','IT'),(5,'Karan Desai','Mech'),(6,'Ananya Iyer','CS'),
(7,'Vikas Rao','Civil'),(8,'Pooja Nair','IT'),(9,'Arjun Tiwari','CS'),
(10,'Neha Gupta','ENTC'),(11,'Raj Malhotra','IT'),(12,'Meera Pillai','Mech'),
(13,'Dev Sharma','CS'),(14,'Tara Jain','IT'),(15,'Yash Kumar','ENTC');

-- Insert 3 professors (3NF)
INSERT INTO NF3_Professors (ProfessorName, Department, Email) VALUES
('Prof. Sharma', 'IT',   'sharma@college.edu'),
('Prof. Verma',  'CS',   'verma@college.edu'),
('Prof. Iyer',   'ENTC', 'iyer@college.edu');

-- Insert 5 courses linked to professors
INSERT INTO NF3_Courses VALUES
('CS101','Data Structures',      4, 1),
('CS102','DBMS',                 4, 2),
('CS103','Operating Systems',    3, 3),
('CS104','Computer Networks',    3, 1),
('CS105','Artificial Intelligence',4,2);

-- DDL: ALTER TABLE demonstrations
ALTER TABLE NF2_Students ADD COLUMN Email VARCHAR(100);
ALTER TABLE NF2_Students MODIFY COLUMN Email VARCHAR(150);
ALTER TABLE NF2_Students ADD COLUMN Phone VARCHAR(15) DEFAULT 'Not Provided';
ALTER TABLE NF2_Students DROP COLUMN Phone;
ALTER TABLE NF2_Students RENAME COLUMN Email TO StudentEmail;

-- Rename a table
RENAME TABLE NF2_Students TO Students;

-- Verify final structure
DESCRIBE Students;
SHOW CREATE TABLE NF3_Courses;"""),

"practical_06_constraints_alter_drop": (
"MySQL 8.x — Constraints, ALTER TABLE & DROP",
"""-- ============================================================
-- Practical 06: Constraints, ALTER TABLE & DROP
-- S.Y.B.Tech IT | Sem IV | Subject: 2308215
-- ============================================================

USE college_db;

-- Create Department table demonstrating all constraint types
CREATE TABLE IF NOT EXISTS Department (
    DeptID          INT           PRIMARY KEY AUTO_INCREMENT,
    DeptName        VARCHAR(50)   NOT NULL UNIQUE,
    Location        VARCHAR(50)   NOT NULL DEFAULT 'Main Campus',
    Budget          DECIMAL(12,2) CHECK (Budget > 0),
    EstablishedYear YEAR          CHECK (EstablishedYear >= 1900)
);

-- Create Employee table with FOREIGN KEY + ON DELETE CASCADE
CREATE TABLE IF NOT EXISTS Employee (
    EmpID    INT           PRIMARY KEY AUTO_INCREMENT,
    EmpName  VARCHAR(100)  NOT NULL,
    Salary   DECIMAL(10,2) NOT NULL CHECK (Salary >= 15000 AND Salary <= 500000),
    JoinDate DATE          DEFAULT (CURRENT_DATE),
    Email    VARCHAR(100)  UNIQUE,
    Gender   ENUM('Male','Female','Other') NOT NULL,
    DeptID   INT           NOT NULL,
    FOREIGN KEY (DeptID) REFERENCES Department(DeptID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Insert 5 departments
INSERT INTO Department (DeptName, Location, Budget, EstablishedYear) VALUES
('Information Technology', 'Building A', 1500000.00, 2000),
('Human Resources',        'Building B',  800000.00, 1995),
('Finance',                'Building C', 2000000.00, 1990),
('Marketing',              'Building D', 1200000.00, 2005),
('Operations',             'Main Campus',1800000.00, 1985);

-- Insert 15 employees
INSERT INTO Employee (EmpName, Salary, Email, Gender, DeptID) VALUES
('Anil Kumar',    45000, 'anil@co.com',    'Male',   1),
('Sunita Rao',    52000, 'sunita@co.com',  'Female', 2),
('Raj Patel',     61000, 'raj@co.com',     'Male',   1),
('Meena Shah',    38000, 'meena@co.com',   'Female', 3),
('Vikram Singh',  70000, 'vikram@co.com',  'Male',   4),
('Pooja Nair',    43000, 'pooja@co.com',   'Female', 2),
('Arjun Tiwari',  55000, 'arjun@co.com',  'Male',   5),
('Kavya Iyer',    48000, 'kavya@co.com',   'Female', 1),
('Ravi Menon',    62000, 'ravi@co.com',    'Male',   3),
('Deepa Joshi',   41000, 'deepa@co.com',   'Female', 4),
('Suresh Pillai', 75000, 'suresh@co.com',  'Male',   5),
('Anita Desai',   44000, 'anita@co.com',   'Female', 2),
('Manoj Verma',   58000, 'manoj@co.com',  'Male',   1),
('Rekha Gupta',   39000, 'rekha@co.com',  'Female', 3),
('Nikhil Sharma', 67000, 'nikhil@co.com', 'Male',   4);

-- ALTER TABLE: Add a new column
ALTER TABLE Employee ADD COLUMN Phone VARCHAR(15);

-- ALTER TABLE: Modify column size
ALTER TABLE Employee MODIFY COLUMN Phone VARCHAR(20) DEFAULT '0000000000';

-- ALTER TABLE: Rename column
ALTER TABLE Employee RENAME COLUMN Phone TO MobileNo;

-- ALTER TABLE: Add a named CHECK constraint
ALTER TABLE Employee ADD CONSTRAINT chk_join
    CHECK (JoinDate >= '2000-01-01');

-- ALTER TABLE: Drop the CHECK constraint
ALTER TABLE Employee DROP CHECK chk_join;

-- ALTER TABLE: Drop the column
ALTER TABLE Employee DROP COLUMN MobileNo;

-- Demonstrate ON DELETE CASCADE
-- Deleting DeptID=5 will auto-delete all Operations employees
DELETE FROM Department WHERE DeptID = 5;
SELECT EmpName, DeptID FROM Employee ORDER BY DeptID;

-- DELETE with WHERE (targeted, can be rolled back)
DELETE FROM Employee WHERE Salary < 40000;

-- Constraint violation examples (these WILL fail — educational)
-- INSERT INTO Employee (EmpName,Salary,Gender,DeptID) VALUES ('X',5000,'Male',1);
-- ERROR 3819: Check constraint 'employee_chk_1' violated (Salary < 15000)

-- TRUNCATE (all rows, AUTO_INCREMENT resets, cannot rollback)
-- TRUNCATE TABLE Employee;

-- DROP (destroys table structure completely)
-- DROP TABLE IF EXISTS Employee;

-- Verify final structure
DESCRIBE Employee;
SHOW CREATE TABLE Employee;

-- List all constraints for the database
SELECT TABLE_NAME, CONSTRAINT_NAME, CONSTRAINT_TYPE
FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS
WHERE TABLE_SCHEMA = 'college_db'
ORDER BY TABLE_NAME;"""),

"practical_07_sql_queries": (
"MySQL 8.x — DML & Advanced SQL Queries",
"""-- ============================================================
-- Practical 07: SQL Queries (DML — SELECT, INSERT, UPDATE, DELETE)
-- S.Y.B.Tech IT | Sem IV | Subject: 2308215
-- ============================================================

USE college_db;

-- ── Basic SELECT ──
SELECT EmpName, Salary, DeptID FROM Employee ORDER BY Salary DESC LIMIT 5;

-- DISTINCT: remove duplicate department IDs
SELECT DISTINCT DeptID FROM Employee;

-- ── WHERE clause operators ──

-- BETWEEN: salary range (inclusive)
SELECT EmpName, Salary FROM Employee WHERE Salary BETWEEN 45000 AND 65000;

-- IN: specific department list
SELECT EmpName, DeptID FROM Employee WHERE DeptID IN (1, 2, 3);

-- NOT IN: exclude departments
SELECT EmpName, DeptID FROM Employee WHERE DeptID NOT IN (4, 5);

-- LIKE patterns (% = any chars, _ = single char)
SELECT EmpName FROM Employee WHERE EmpName LIKE 'A%';
SELECT EmpName FROM Employee WHERE EmpName LIKE '%ar%';
SELECT EmpName FROM Employee WHERE EmpName LIKE '_____';

-- IS NOT NULL / IS NULL
SELECT EmpName FROM Employee WHERE Email IS NOT NULL;

-- AND / OR combinations
SELECT EmpName, Salary FROM Employee WHERE DeptID = 1 AND Salary > 50000;
SELECT EmpName FROM Employee WHERE DeptID = 1 OR DeptID = 2;

-- ── Aggregate Functions ──
SELECT COUNT(*)         AS TotalEmp,
       SUM(Salary)      AS TotalSalary,
       AVG(Salary)      AS AvgSalary,
       MAX(Salary)      AS MaxSalary,
       MIN(Salary)      AS MinSalary
FROM Employee;

-- ── GROUP BY with HAVING ──
SELECT DeptID,
       COUNT(*)             AS EmpCount,
       ROUND(AVG(Salary),2) AS AvgSal
FROM Employee
GROUP BY DeptID
HAVING AVG(Salary) > 50000;

-- ── WITH ROLLUP: subtotals + grand total ──
SELECT DeptID, COUNT(*) AS Count, SUM(Salary) AS Total
FROM Employee
GROUP BY DeptID WITH ROLLUP;

-- ── Subqueries ──

-- 1. Scalar subquery: employees earning above company average
SELECT EmpName, Salary FROM Employee
WHERE Salary > (SELECT AVG(Salary) FROM Employee);

-- 2. Derived table (subquery in FROM clause)
SELECT DeptID, AvgSal
FROM (
    SELECT DeptID, AVG(Salary) AS AvgSal
    FROM Employee
    GROUP BY DeptID
) AS DeptAvg
WHERE AvgSal > 50000;

-- 3. Correlated subquery: top earner per department
SELECT EmpName, Salary, DeptID FROM Employee E1
WHERE Salary = (
    SELECT MAX(Salary) FROM Employee E2
    WHERE E2.DeptID = E1.DeptID
);

-- 4. Scalar subquery in SELECT column
SELECT EmpName, Salary,
       (SELECT AVG(Salary) FROM Employee) AS CompanyAvg
FROM Employee;

-- 5. EXISTS subquery
SELECT DeptName FROM Department D
WHERE EXISTS (
    SELECT 1 FROM Employee E WHERE E.DeptID = D.DeptID
);

-- 6. NOT IN: departments with no employees
SELECT DeptName FROM Department
WHERE DeptID NOT IN (SELECT DISTINCT DeptID FROM Employee);

-- ── Set Operations ──

-- UNION (removes duplicates)
SELECT EmpName, Salary FROM Employee WHERE Salary > 65000
UNION
SELECT EmpName, Salary FROM Employee WHERE DeptID = 1;

-- UNION ALL (keeps duplicates)
SELECT EmpName FROM Employee WHERE DeptID = 1
UNION ALL
SELECT EmpName FROM Employee WHERE Salary > 55000;

-- INTERSECT simulated: dept 1 AND salary > 50000
SELECT EmpName FROM Employee WHERE DeptID = 1
AND EmpID IN (SELECT EmpID FROM Employee WHERE Salary > 50000);

-- MINUS simulated: dept 1 but NOT earning > 65000
SELECT EmpName FROM Employee WHERE DeptID = 1
AND EmpID NOT IN (SELECT EmpID FROM Employee WHERE Salary > 65000);

-- ── String Functions ──
SELECT CONCAT(EmpName, ' | Dept: ', DeptID) AS Info FROM Employee;
SELECT UPPER(EmpName), LENGTH(EmpName) AS NameLen FROM Employee;

-- ── UPDATE: 10% salary raise for dept 1 ──
UPDATE Employee SET Salary = Salary * 1.10 WHERE DeptID = 1;

-- ── DELETE specific rows ──
DELETE FROM Employee WHERE Salary < 38000;

-- Verify final state
SELECT DeptID, COUNT(*) AS Remaining FROM Employee GROUP BY DeptID;"""),

"practical_08_views": (
"MySQL 8.x — Views & Virtual Tables",
"""-- ============================================================
-- Practical 08: Views
-- S.Y.B.Tech IT | Sem IV | Subject: 2308215
-- ============================================================

USE college_db;

-- View 1: Simple view — IT department employees only
CREATE OR REPLACE VIEW IT_Employees AS
SELECT EmpID, EmpName, Salary, Email
FROM Employee
WHERE DeptID = 1;

SELECT * FROM IT_Employees;

-- View 2: JOIN view — employees with department details
CREATE OR REPLACE VIEW Employee_Full_Details AS
SELECT E.EmpID, E.EmpName, E.Salary, E.Gender, E.Email,
       D.DeptName, D.Location, D.Budget
FROM Employee E
INNER JOIN Department D ON E.DeptID = D.DeptID;

SELECT * FROM Employee_Full_Details WHERE Salary > 50000;

-- View 3: Aggregate view — department salary statistics
CREATE OR REPLACE VIEW Department_Summary AS
SELECT D.DeptName,
       COUNT(E.EmpID)          AS TotalEmployees,
       ROUND(AVG(E.Salary), 2) AS AvgSalary,
       SUM(E.Salary)           AS TotalSalaryBill,
       MAX(E.Salary)           AS TopSalary,
       MIN(E.Salary)           AS LowestSalary
FROM Department D
LEFT JOIN Employee E ON D.DeptID = E.DeptID
GROUP BY D.DeptName, D.DeptID;

SELECT * FROM Department_Summary ORDER BY TotalSalaryBill DESC;

-- View 4: Security view — hide salary column
CREATE OR REPLACE VIEW Employee_Public_Info AS
SELECT EmpID, EmpName, Gender, Email, DeptID
FROM Employee;

-- View 5: Updatable view WITH CHECK OPTION
CREATE OR REPLACE VIEW HighSalary_Employees AS
SELECT EmpID, EmpName, Salary, DeptID
FROM Employee
WHERE Salary > 50000
WITH CHECK OPTION;

-- Valid update: salary stays above 50000 (allowed)
UPDATE HighSalary_Employees SET Salary = 72000 WHERE EmpID = 3;

-- This would FAIL with CHECK OPTION (salary drops below 50000):
-- UPDATE HighSalary_Employees SET Salary = 25000 WHERE EmpID = 3;
-- ERROR 1369: CHECK OPTION failed

-- Update view definition without dropping it
CREATE OR REPLACE VIEW IT_Employees AS
SELECT EmpID, EmpName, Salary, Email, Gender
FROM Employee WHERE DeptID = 1;

-- List all views in the current database
SHOW FULL TABLES WHERE Table_type = 'VIEW';

-- Show the DDL used to create a specific view
SHOW CREATE VIEW Department_Summary;

-- View metadata from INFORMATION_SCHEMA
SELECT TABLE_NAME      AS ViewName,
       IS_UPDATABLE,
       SECURITY_TYPE
FROM INFORMATION_SCHEMA.VIEWS
WHERE TABLE_SCHEMA = 'college_db';

-- Drop a view that is no longer needed
DROP VIEW IF EXISTS Employee_Public_Info;

-- Verify remaining views
SHOW FULL TABLES WHERE Table_type = 'VIEW';"""),

"practical_09_implementation_of_joins": (
"MySQL 8.x — Implementation of Joins",
"""-- ============================================================
-- Practical 09: Implementation of All JOIN Types
-- S.Y.B.Tech IT | Sem IV | Subject: 2308215
-- ============================================================

USE college_db;

-- Add ManagerID column for SELF JOIN demonstration
ALTER TABLE Employee ADD COLUMN IF NOT EXISTS ManagerID INT;
UPDATE Employee SET ManagerID = 1 WHERE EmpID IN (2,3,4,5,6);
UPDATE Employee SET ManagerID = 2 WHERE EmpID IN (7,8,9);
UPDATE Employee SET ManagerID = 3 WHERE EmpID IN (10,11,12);

-- Create Projects table for multi-table JOIN
CREATE TABLE IF NOT EXISTS Project (
    ProjectID   INT           PRIMARY KEY AUTO_INCREMENT,
    ProjectName VARCHAR(100)  NOT NULL,
    Budget      DECIMAL(12,2),
    DeptID      INT,
    FOREIGN KEY (DeptID) REFERENCES Department(DeptID)
);

INSERT INTO Project (ProjectName, Budget, DeptID) VALUES
('ERP System',       500000, 1),
('HR Portal',        200000, 2),
('Budget Tracker',   350000, 3),
('Campaign Manager', 150000, 4),
('Ops Dashboard',    400000, 1);

-- 1. INNER JOIN: matched rows only (employees WITH a valid department)
SELECT E.EmpName, E.Salary, D.DeptName, D.Location
FROM Employee E
INNER JOIN Department D ON E.DeptID = D.DeptID
ORDER BY D.DeptName;

-- 2. LEFT JOIN: ALL departments including those with no employees
SELECT D.DeptName, E.EmpName, E.Salary
FROM Department D
LEFT JOIN Employee E ON D.DeptID = E.DeptID
ORDER BY D.DeptName;

-- 3. RIGHT JOIN: ALL employees regardless of department existence
SELECT D.DeptName, E.EmpName, E.Salary
FROM Department D
RIGHT JOIN Employee E ON D.DeptID = E.DeptID;

-- 4. FULL OUTER JOIN simulated with UNION of LEFT + RIGHT
SELECT D.DeptName, E.EmpName
FROM Department D LEFT JOIN Employee E ON D.DeptID = E.DeptID
UNION
SELECT D.DeptName, E.EmpName
FROM Department D RIGHT JOIN Employee E ON D.DeptID = E.DeptID;

-- 5. SELF JOIN: employee and their manager from the same table
SELECT E.EmpName AS Employee,
       M.EmpName AS Manager,
       E.Salary  AS EmpSalary
FROM Employee E
LEFT JOIN Employee M ON E.ManagerID = M.EmpID
ORDER BY Manager;

-- 6. CROSS JOIN: Cartesian product (every employee × every project)
SELECT E.EmpName, P.ProjectName
FROM Employee E
CROSS JOIN Project P
LIMIT 20;

-- 7. Three-table JOIN: Employee + Department + Project
SELECT E.EmpName, D.DeptName, P.ProjectName, P.Budget
FROM Employee E
JOIN Department D ON E.DeptID   = D.DeptID
JOIN Project  P  ON D.DeptID   = P.DeptID
ORDER BY D.DeptName;

-- 8. JOIN with WHERE filter
SELECT E.EmpName, D.DeptName, E.Salary
FROM Employee E
JOIN Department D ON E.DeptID = D.DeptID
WHERE E.Salary > 55000
  AND D.DeptName = 'Information Technology';

-- 9. JOIN with GROUP BY aggregate
SELECT D.DeptName,
       COUNT(E.EmpID)          AS Headcount,
       ROUND(AVG(E.Salary), 2) AS AvgSalary,
       SUM(E.Salary)           AS SalaryBill
FROM Department D
LEFT JOIN Employee E ON D.DeptID = E.DeptID
GROUP BY D.DeptName
ORDER BY SalaryBill DESC;"""),

"practical_10_stored_procedures": (
"MySQL 8.x — Stored Procedures & User-Defined Functions",
"""-- ============================================================
-- Practical 10: Stored Procedures & Functions
-- S.Y.B.Tech IT | Sem IV | Subject: 2308215
-- ============================================================

USE college_db;
DELIMITER $$

-- ── PROCEDURE 1: IN parameter ──
CREATE PROCEDURE GetEmployeesByDept(IN p_DeptID INT)
BEGIN
    SELECT EmpID, EmpName, Salary, Email
    FROM Employee
    WHERE DeptID = p_DeptID
    ORDER BY Salary DESC;
END$$

CALL GetEmployeesByDept(1)$$

-- ── PROCEDURE 2: OUT parameters ──
CREATE PROCEDURE GetDeptStats(
    IN  p_DeptID    INT,
    OUT p_Count     INT,
    OUT p_AvgSalary DECIMAL(10,2),
    OUT p_MaxSalary DECIMAL(10,2)
)
BEGIN
    SELECT COUNT(*), ROUND(AVG(Salary),2), MAX(Salary)
    INTO   p_Count, p_AvgSalary, p_MaxSalary
    FROM   Employee
    WHERE  DeptID = p_DeptID;
END$$

CALL GetDeptStats(1, @cnt, @avg, @mx)$$
SELECT @cnt AS EmpCount, @avg AS AvgSalary, @mx AS MaxSalary$$

-- ── PROCEDURE 3: INOUT parameter ──
CREATE PROCEDURE ApplyBonus(
    INOUT p_Salary  DECIMAL(10,2),
    IN    p_Percent DECIMAL(5,2)
)
BEGIN
    SET p_Salary = p_Salary + (p_Salary * p_Percent / 100);
END$$

SET @sal = 50000$$
CALL ApplyBonus(@sal, 15)$$
SELECT @sal AS SalaryAfter15PctBonus$$

-- ── PROCEDURE 4: IF-ELSEIF-ELSE grading ──
CREATE PROCEDURE GetEmpGrade(IN p_EmpID INT)
BEGIN
    DECLARE v_Salary DECIMAL(10,2);
    DECLARE v_Name   VARCHAR(100);
    DECLARE v_Grade  VARCHAR(20);

    SELECT EmpName, Salary INTO v_Name, v_Salary
    FROM Employee WHERE EmpID = p_EmpID;

    IF     v_Salary >= 70000 THEN SET v_Grade = 'A - Executive';
    ELSEIF v_Salary >= 55000 THEN SET v_Grade = 'B - Senior';
    ELSEIF v_Salary >= 40000 THEN SET v_Grade = 'C - Mid-Level';
    ELSE                          SET v_Grade = 'D - Junior';
    END IF;

    SELECT v_Name AS Name, v_Salary AS Salary, v_Grade AS Grade;
END$$

CALL GetEmpGrade(5)$$

-- ── PROCEDURE 5: WHILE LOOP — 5-year salary projection ──
CREATE PROCEDURE SalaryProjection(IN p_EmpID INT, IN p_Years INT)
BEGIN
    DECLARE v_Year   INT DEFAULT 1;
    DECLARE v_Salary DECIMAL(10,2);

    SELECT Salary INTO v_Salary FROM Employee WHERE EmpID = p_EmpID;

    DROP TEMPORARY TABLE IF EXISTS Projection;
    CREATE TEMPORARY TABLE Projection (Year INT, ProjectedSalary DECIMAL(10,2));

    WHILE v_Year <= p_Years DO
        SET v_Salary = ROUND(v_Salary * 1.08, 2);
        INSERT INTO Projection VALUES (v_Year, v_Salary);
        SET v_Year = v_Year + 1;
    END WHILE;

    SELECT * FROM Projection;
END$$

CALL SalaryProjection(1, 5)$$

-- ── FUNCTION 1: Income tax calculation ──
CREATE FUNCTION CalcTax(p_Salary DECIMAL(10,2))
RETURNS DECIMAL(10,2) DETERMINISTIC
BEGIN
    IF     p_Salary > 80000 THEN RETURN ROUND(p_Salary * 0.30, 2);
    ELSEIF p_Salary > 50000 THEN RETURN ROUND(p_Salary * 0.20, 2);
    ELSE                         RETURN ROUND(p_Salary * 0.10, 2);
    END IF;
END$$

SELECT EmpName, Salary,
       CalcTax(Salary)           AS TaxAmount,
       Salary - CalcTax(Salary)  AS TakeHome
FROM Employee$$

-- ── FUNCTION 2: Experience level from join date ──
CREATE FUNCTION ExperienceLevel(p_JoinDate DATE)
RETURNS VARCHAR(20) DETERMINISTIC
BEGIN
    DECLARE v_Years INT;
    SET v_Years = TIMESTAMPDIFF(YEAR, p_JoinDate, CURDATE());

    IF     v_Years >= 10 THEN RETURN 'Veteran';
    ELSEIF v_Years >= 5  THEN RETURN 'Experienced';
    ELSEIF v_Years >= 2  THEN RETURN 'Intermediate';
    ELSE                      RETURN 'Fresher';
    END IF;
END$$

SELECT EmpName, JoinDate, ExperienceLevel(JoinDate) AS Level
FROM Employee$$

-- ── PROCEDURE with ERROR HANDLER ──
CREATE PROCEDURE SafeInsert(
    IN p_Name   VARCHAR(100),
    IN p_Salary DECIMAL(10,2),
    IN p_DeptID INT
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT 'Insert failed: constraint violation or invalid data' AS ErrorMsg;
    END;

    START TRANSACTION;
    INSERT INTO Employee (EmpName, Salary, Gender, DeptID)
    VALUES (p_Name, p_Salary, 'Male', p_DeptID);
    COMMIT;
    SELECT CONCAT(p_Name, ' added successfully') AS Status;
END$$

CALL SafeInsert('Valid Employee', 45000, 1)$$
CALL SafeInsert('Bad Pay Emp',     1000, 99)$$

DELIMITER ;

-- Show all procedures in the database
SHOW PROCEDURE STATUS WHERE Db = 'college_db';"""),

"practical_11_triggers": (
"MySQL 8.x — Triggers & Audit Logging",
"""-- ============================================================
-- Practical 11: Triggers
-- S.Y.B.Tech IT | Sem IV | Subject: 2308215
-- ============================================================

USE college_db;

-- Audit table to record all DML changes on Employee
CREATE TABLE IF NOT EXISTS Employee_Audit (
    AuditID   INT          PRIMARY KEY AUTO_INCREMENT,
    EmpID     INT,
    Action    VARCHAR(10)  NOT NULL,
    OldName   VARCHAR(100), NewName   VARCHAR(100),
    OldSalary DECIMAL(10,2), NewSalary DECIMAL(10,2),
    OldDeptID INT,           NewDeptID INT,
    ChangedBy VARCHAR(100),
    ChangedAt DATETIME     DEFAULT CURRENT_TIMESTAMP
);

DELIMITER $$

-- TRIGGER 1: BEFORE INSERT — validate salary & auto-format name
CREATE TRIGGER trg_before_insert_emp
BEFORE INSERT ON Employee FOR EACH ROW
BEGIN
    IF NEW.Salary < 15000 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Salary must be at least 15000';
    END IF;
    SET NEW.EmpName = CONCAT(
        UPPER(LEFT(NEW.EmpName, 1)),
        LOWER(SUBSTRING(NEW.EmpName, 2))
    );
END$$

-- TRIGGER 2: AFTER INSERT — log new employee
CREATE TRIGGER trg_after_insert_emp
AFTER INSERT ON Employee FOR EACH ROW
BEGIN
    INSERT INTO Employee_Audit
        (EmpID, Action, NewName, NewSalary, NewDeptID, ChangedBy)
    VALUES
        (NEW.EmpID, 'INSERT', NEW.EmpName, NEW.Salary, NEW.DeptID, USER());
END$$

-- TRIGGER 3: BEFORE UPDATE — prevent salary reduction
CREATE TRIGGER trg_before_update_emp
BEFORE UPDATE ON Employee FOR EACH ROW
BEGIN
    IF NEW.Salary < OLD.Salary THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Salary cannot be reduced';
    END IF;
    -- Auto-update JoinDate when employee transfers department
    IF NEW.DeptID != OLD.DeptID THEN
        SET NEW.JoinDate = CURDATE();
    END IF;
END$$

-- TRIGGER 4: AFTER UPDATE — log all changes
CREATE TRIGGER trg_after_update_emp
AFTER UPDATE ON Employee FOR EACH ROW
BEGIN
    INSERT INTO Employee_Audit
        (EmpID, Action, OldName, NewName,
         OldSalary, NewSalary, OldDeptID, NewDeptID, ChangedBy)
    VALUES
        (NEW.EmpID, 'UPDATE', OLD.EmpName, NEW.EmpName,
         OLD.Salary, NEW.Salary, OLD.DeptID, NEW.DeptID, USER());
END$$

-- TRIGGER 5: BEFORE DELETE — protect executives (salary > 90000)
CREATE TRIGGER trg_before_delete_emp
BEFORE DELETE ON Employee FOR EACH ROW
BEGIN
    IF OLD.Salary > 90000 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Cannot delete employee with salary above 90000';
    END IF;
END$$

-- TRIGGER 6: AFTER DELETE — log deletion
CREATE TRIGGER trg_after_delete_emp
AFTER DELETE ON Employee FOR EACH ROW
BEGIN
    INSERT INTO Employee_Audit
        (EmpID, Action, OldName, OldSalary, OldDeptID, ChangedBy)
    VALUES
        (OLD.EmpID, 'DELETE', OLD.EmpName, OLD.Salary, OLD.DeptID, USER());
END$$

DELIMITER ;

-- TEST 1: Valid insert (name auto-formatted by BEFORE INSERT trigger)
INSERT INTO Employee (EmpName, Salary, Gender, DeptID)
VALUES ('rAHUL sharma', 35000, 'Male', 1);

-- View audit log after insert
SELECT * FROM Employee_Audit;

-- TEST 2: Valid salary update (BEFORE UPDATE allows, AFTER UPDATE logs)
UPDATE Employee SET Salary = 60000 WHERE EmpName = 'Rahul Sharma';
SELECT * FROM Employee_Audit ORDER BY ChangedAt DESC LIMIT 5;

-- TEST 3: Delete employee (BEFORE DELETE allows, AFTER DELETE logs)
DELETE FROM Employee WHERE EmpName = 'Rahul Sharma';
SELECT * FROM Employee_Audit ORDER BY AuditID DESC LIMIT 5;

-- TEST 4: Invalid salary triggers BEFORE INSERT error
-- INSERT INTO Employee (EmpName, Salary, Gender, DeptID)
-- VALUES ('Test', 5000, 'Male', 1);
-- ERROR 1644: Salary must be at least 15000

-- Show all triggers in the database
SHOW TRIGGERS FROM college_db;"""),

"practical_12_cursors": (
"MySQL 8.x — Cursors",
"""-- ============================================================
-- Practical 12: Cursors
-- S.Y.B.Tech IT | Sem IV | Subject: 2308215
-- ============================================================

USE college_db;
DELIMITER $$

-- CURSOR 1: Categorize all employees by salary band
CREATE PROCEDURE CategorizeAllEmployees()
BEGIN
    DECLARE v_EmpID    INT;
    DECLARE v_Name     VARCHAR(100);
    DECLARE v_Salary   DECIMAL(10,2);
    DECLARE v_DeptID   INT;
    DECLARE v_Category VARCHAR(30);
    DECLARE v_Done     INT DEFAULT FALSE;

    -- Declare cursor AFTER all variable declarations
    DECLARE emp_cursor CURSOR FOR
        SELECT EmpID, EmpName, Salary, DeptID
        FROM Employee
        ORDER BY DeptID, Salary DESC;

    -- NOT FOUND handler MUST be declared after cursor
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET v_Done = TRUE;

    DROP TEMPORARY TABLE IF EXISTS EmpReport;
    CREATE TEMPORARY TABLE EmpReport (
        EmpID    INT,
        Name     VARCHAR(100),
        Salary   DECIMAL(10,2),
        DeptID   INT,
        Category VARCHAR(30)
    );

    OPEN emp_cursor;

    process_loop: LOOP
        FETCH emp_cursor INTO v_EmpID, v_Name, v_Salary, v_DeptID;
        IF v_Done THEN LEAVE process_loop; END IF;

        -- Per-row business logic: assign salary band
        IF     v_Salary >= 70000 THEN SET v_Category = 'Executive';
        ELSEIF v_Salary >= 55000 THEN SET v_Category = 'Senior';
        ELSEIF v_Salary >= 40000 THEN SET v_Category = 'Mid-Level';
        ELSE                          SET v_Category = 'Junior';
        END IF;

        INSERT INTO EmpReport
        VALUES (v_EmpID, v_Name, v_Salary, v_DeptID, v_Category);
    END LOOP;

    CLOSE emp_cursor;

    -- Full categorized report
    SELECT * FROM EmpReport ORDER BY DeptID, Salary DESC;

    -- Summary: count and avg salary per category
    SELECT Category,
           COUNT(*) AS Count,
           ROUND(AVG(Salary), 2) AS AvgSalary
    FROM EmpReport
    GROUP BY Category
    ORDER BY AvgSalary DESC;
END$$

CALL CategorizeAllEmployees()$$

-- ──────────────────────────────────────────────────────────

-- CURSOR 2: Department-wise running salary total
CREATE PROCEDURE DeptRunningTotal()
BEGIN
    DECLARE v_EmpName     VARCHAR(100);
    DECLARE v_Salary      DECIMAL(10,2);
    DECLARE v_DeptName    VARCHAR(50);
    DECLARE v_Running     DECIMAL(12,2) DEFAULT 0;
    DECLARE v_CurrentDept VARCHAR(50)   DEFAULT '';
    DECLARE v_Done        INT DEFAULT FALSE;

    DECLARE dept_cursor CURSOR FOR
        SELECT E.EmpName, E.Salary, D.DeptName
        FROM Employee E
        JOIN Department D ON E.DeptID = D.DeptID
        ORDER BY D.DeptName, E.Salary DESC;

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET v_Done = TRUE;

    DROP TEMPORARY TABLE IF EXISTS RunningTotals;
    CREATE TEMPORARY TABLE RunningTotals (
        DeptName       VARCHAR(50),
        EmpName        VARCHAR(100),
        Salary         DECIMAL(10,2),
        RunningDeptTotal DECIMAL(12,2)
    );

    OPEN dept_cursor;

    dept_loop: LOOP
        FETCH dept_cursor INTO v_EmpName, v_Salary, v_DeptName;
        IF v_Done THEN LEAVE dept_loop; END IF;

        -- Reset running total when department changes
        IF v_DeptName != v_CurrentDept THEN
            SET v_Running     = 0;
            SET v_CurrentDept = v_DeptName;
        END IF;

        SET v_Running = v_Running + v_Salary;
        INSERT INTO RunningTotals
        VALUES (v_DeptName, v_EmpName, v_Salary, v_Running);
    END LOOP;

    CLOSE dept_cursor;
    SELECT * FROM RunningTotals;
END$$

CALL DeptRunningTotal()$$

DELIMITER ;"""),

"practical_13_project_proposal_srs": (
"MySQL 8.x — Library Management System (Project Proposal & SRS)",
"""-- ============================================================
-- Practical 13: Project Proposal / SRS Implementation
-- Project: Library Management System
-- S.Y.B.Tech IT | Sem IV | Subject: 2308215
-- ============================================================

CREATE DATABASE IF NOT EXISTS library_db;
USE library_db;

-- Entity 1: Member
CREATE TABLE Member (
    MemberID        INT          PRIMARY KEY AUTO_INCREMENT,
    FullName        VARCHAR(100) NOT NULL,
    Email           VARCHAR(100) UNIQUE NOT NULL,
    Phone           VARCHAR(15)  NOT NULL,
    MemberType      ENUM('Student','Faculty','Staff') DEFAULT 'Student',
    JoinDate        DATE         DEFAULT (CURRENT_DATE),
    ExpiryDate      DATE,
    IsActive        BOOLEAN      DEFAULT TRUE,
    MaxBooksAllowed INT          DEFAULT 3
);

-- Entity 2: Book
CREATE TABLE Book (
    BookID          INT          PRIMARY KEY AUTO_INCREMENT,
    ISBN            VARCHAR(20)  UNIQUE NOT NULL,
    Title           VARCHAR(200) NOT NULL,
    Author          VARCHAR(100) NOT NULL,
    Publisher       VARCHAR(100),
    PublishYear     YEAR,
    Category        VARCHAR(50),
    TotalCopies     INT          DEFAULT 1 CHECK (TotalCopies >= 0),
    AvailableCopies INT          DEFAULT 1 CHECK (AvailableCopies >= 0),
    ShelfLocation   VARCHAR(20)
);

-- Entity 3: Librarian
CREATE TABLE Librarian (
    LibID        INT          PRIMARY KEY AUTO_INCREMENT,
    Name         VARCHAR(100) NOT NULL,
    Username     VARCHAR(50)  UNIQUE NOT NULL,
    PasswordHash VARCHAR(255) NOT NULL,
    LastLogin    DATETIME
);

-- Entity 4: Borrowing  (links Member ↔ Book via Librarian)
CREATE TABLE Borrowing (
    BorrowID   INT          PRIMARY KEY AUTO_INCREMENT,
    MemberID   INT          NOT NULL,
    BookID     INT          NOT NULL,
    LibID      INT,
    BorrowDate DATE         DEFAULT (CURRENT_DATE),
    DueDate    DATE         NOT NULL,
    ReturnDate DATE,
    FineAmount DECIMAL(6,2) DEFAULT 0.00,
    Status     ENUM('Active','Returned','Overdue') DEFAULT 'Active',
    FOREIGN KEY (MemberID) REFERENCES Member(MemberID),
    FOREIGN KEY (BookID)   REFERENCES Book(BookID),
    FOREIGN KEY (LibID)    REFERENCES Librarian(LibID)
);

-- Insert 15 members
INSERT INTO Member (FullName, Email, Phone, MemberType, ExpiryDate) VALUES
('Aarav Shah',    'aarav@lib.com',    '9876501001', 'Student', '2025-12-31'),
('Priya Mehta',   'priya@lib.com',    '9876501002', 'Faculty', '2026-12-31'),
('Rohit Joshi',   'rohit@lib.com',    '9876501003', 'Student', '2025-12-31'),
('Sneha Patil',   'sneha@lib.com',    '9876501004', 'Staff',   '2026-06-30'),
('Karan Desai',   'karan@lib.com',    '9876501005', 'Student', '2025-12-31'),
('Ananya Iyer',   'ananya@lib.com',   '9876501006', 'Student', '2025-12-31'),
('Vikas Rao',     'vikas@lib.com',    '9876501007', 'Faculty', '2026-12-31'),
('Pooja Nair',    'pooja@lib.com',    '9876501008', 'Student', '2025-12-31'),
('Arjun Tiwari',  'arjun@lib.com',    '9876501009', 'Staff',   '2026-06-30'),
('Neha Gupta',    'neha@lib.com',     '9876501010', 'Student', '2025-12-31'),
('Raj Malhotra',  'raj@lib.com',      '9876501011', 'Student', '2025-12-31'),
('Meera Pillai',  'meera@lib.com',    '9876501012', 'Faculty', '2026-12-31'),
('Dev Sharma',    'dev@lib.com',      '9876501013', 'Student', '2025-12-31'),
('Tara Jain',     'tara@lib.com',     '9876501014', 'Student', '2025-12-31'),
('Yash Kumar',    'yash@lib.com',     '9876501015', 'Staff',   '2026-06-30');

-- Insert 10 books
INSERT INTO Book (ISBN, Title, Author, Category, TotalCopies, AvailableCopies, ShelfLocation) VALUES
('978-0-13-110362-7','The C Programming Language',    'Kernighan & Ritchie','Programming', 5,3,'A-01'),
('978-0-13-468599-1','Database System Concepts',      'Silberschatz',       'DBMS',        8,5,'B-03'),
('978-0-13-235088-4','Computer Networks',             'Tanenbaum',          'Networking',  4,4,'C-02'),
('978-0-262-03384-8','Introduction to Algorithms',    'Cormen',             'Algorithms',  6,2,'A-05'),
('978-0-13-597444-0','Operating System Concepts',     'Silberschatz',       'OS',          7,6,'B-01'),
('978-1-491-95038-8','Python Data Science Handbook',  'VanderPlas',         'Data Science',3,3,'D-04'),
('978-0-13-110370-2','Clean Code',                    'Robert Martin',      'Soft Engg',   5,4,'A-08'),
('978-0-13-235089-1','Artificial Intelligence',       'Russell & Norvig',   'AI',          4,1,'D-02'),
('978-1-119-54774-8','Machine Learning',              'Alpaydin',           'ML',          3,2,'D-03'),
('978-0-13-468600-4','Computer Organization',         'Patterson',          'Architecture',5,5,'C-05');

-- FR-03: Search books by title or author
SELECT BookID, Title, Author, AvailableCopies, ShelfLocation
FROM Book
WHERE Title LIKE '%Algorithm%' OR Author LIKE '%Silber%';

-- FR-04: Issue a book (decrease available copies)
INSERT INTO Borrowing (MemberID, BookID, LibID, DueDate)
VALUES (1, 4, 1, DATE_ADD(CURDATE(), INTERVAL 14 DAY));
UPDATE Book SET AvailableCopies = AvailableCopies - 1 WHERE BookID = 4;

-- FR-09: Overdue books with automatic fine (Rs 5/day)
SELECT M.FullName, B.Title, BR.DueDate,
       DATEDIFF(CURDATE(), BR.DueDate)     AS DaysOverdue,
       DATEDIFF(CURDATE(), BR.DueDate) * 5 AS FineRs
FROM Borrowing BR
JOIN Member M ON BR.MemberID = M.MemberID
JOIN Book   B ON BR.BookID   = B.BookID
WHERE BR.ReturnDate IS NULL
  AND BR.DueDate < CURDATE();

-- FR-08: Member borrowing history
SELECT B.Title, BR.BorrowDate, BR.DueDate,
       BR.ReturnDate, IFNULL(BR.FineAmount,0) AS Fine, BR.Status
FROM Borrowing BR
JOIN Book B ON BR.BookID = B.BookID
WHERE BR.MemberID = 1
ORDER BY BR.BorrowDate DESC;

-- FR-10: Most borrowed books report
SELECT B.Title, B.Author,
       COUNT(BR.BorrowID) AS TimesBorrowed
FROM Book B
LEFT JOIN Borrowing BR ON B.BookID = BR.BookID
GROUP BY B.BookID
ORDER BY TimesBorrowed DESC
LIMIT 5;"""),

"practical_14_er_diagram_database_design": (
"MySQL 8.x — Indexes, Transactions & Query Optimization",
"""-- ============================================================
-- Practical 14: ER Diagram & Final Database Design
-- Indexes, Transactions, EXPLAIN Analysis
-- S.Y.B.Tech IT | Sem IV | Subject: 2308215
-- ============================================================

USE college_db;

-- ── INDEXES ──

-- View existing indexes on Employee table
SHOW INDEX FROM Employee;

-- Single-column index for salary range queries
CREATE INDEX idx_emp_salary
    ON Employee(Salary);

-- Composite index for dept + salary queries (leftmost prefix rule)
CREATE INDEX idx_emp_dept_salary
    ON Employee(DeptID, Salary);

-- Index on join date for date-range reports
CREATE INDEX idx_emp_joindate
    ON Employee(JoinDate);

-- EXPLAIN: verify composite index is used (type should be 'ref' or 'range')
EXPLAIN
SELECT * FROM Employee WHERE DeptID = 1 AND Salary > 50000;

-- EXPLAIN: salary range query
EXPLAIN
SELECT EmpName FROM Employee WHERE Salary BETWEEN 40000 AND 70000;

-- EXPLAIN: JOIN query — verify DeptID FK index is used
EXPLAIN
SELECT E.EmpName, D.DeptName
FROM Employee E
JOIN Department D ON E.DeptID = D.DeptID
WHERE D.DeptName = 'Information Technology';

-- List all indexes in college_db from INFORMATION_SCHEMA
SELECT TABLE_NAME, INDEX_NAME, COLUMN_NAME,
       SEQ_IN_INDEX, NON_UNIQUE
FROM INFORMATION_SCHEMA.STATISTICS
WHERE TABLE_SCHEMA = 'college_db'
ORDER BY TABLE_NAME, INDEX_NAME, SEQ_IN_INDEX;

-- Drop an index made redundant by the composite index
DROP INDEX idx_emp_joindate ON Employee;

-- ── TRANSACTIONS ──

-- Transaction 1: Atomic salary bonus transfer
START TRANSACTION;
    UPDATE Employee SET Salary = Salary - 3000 WHERE EmpID = 1;
    UPDATE Employee SET Salary = Salary + 3000 WHERE EmpID = 2;
    SELECT EmpID, EmpName, Salary FROM Employee WHERE EmpID IN (1, 2);
COMMIT;

-- Transaction 2: SAVEPOINT — partial rollback
START TRANSACTION;
    INSERT INTO Employee (EmpName, Salary, Gender, DeptID)
    VALUES ('Temp Alpha', 32000, 'Male', 1);
    SAVEPOINT after_alpha;

    INSERT INTO Employee (EmpName, Salary, Gender, DeptID)
    VALUES ('Temp Beta', 36000, 'Female', 2);
    SAVEPOINT after_beta;

    INSERT INTO Employee (EmpName, Salary, Gender, DeptID)
    VALUES ('Temp Gamma', 29000, 'Male', 3);

    -- Undo only Gamma; keep Alpha and Beta
    ROLLBACK TO SAVEPOINT after_beta;
COMMIT;

SELECT EmpName FROM Employee WHERE EmpName LIKE 'Temp%';

-- Transaction 3: Full ROLLBACK demonstration
START TRANSACTION;
    DELETE FROM Employee WHERE DeptID = 4;
    SELECT COUNT(*) AS RemainingInDept4 FROM Employee WHERE DeptID = 4;
ROLLBACK;
SELECT COUNT(*) AS RestoredDept4Count FROM Employee WHERE DeptID = 4;

-- Set isolation level for next session
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;

-- Final optimized departmental report with EXPLAIN
EXPLAIN
SELECT D.DeptName,
       COUNT(E.EmpID)          AS Headcount,
       ROUND(AVG(E.Salary),2)  AS AvgSalary,
       SUM(E.Salary)           AS TotalBill,
       MAX(E.Salary)           AS TopEarner
FROM Department D
LEFT JOIN Employee E ON D.DeptID = E.DeptID
GROUP BY D.DeptName
ORDER BY TotalBill DESC;

-- Run the actual final report
SELECT D.DeptName,
       COUNT(E.EmpID)          AS Headcount,
       ROUND(AVG(E.Salary),2)  AS AvgSalary,
       SUM(E.Salary)           AS TotalBill,
       MAX(E.Salary)           AS TopEarner
FROM Department D
LEFT JOIN Employee E ON D.DeptID = E.DeptID
GROUP BY D.DeptName
ORDER BY TotalBill DESC;"""),

}  # end CODES dict


# ─── Patch every HTML file ────────────────────────────────────────────────────

def replace_code_block(path, label, sql):
    with open(path, encoding='utf-8') as f:
        content = f.read()

    # Find the traffic-light terminal div
    dot_start = content.find('<div class="bg-[#0a0e14]')
    if dot_start == -1:
        print(f"  ⚠  Terminal div not found in {path}")
        return

    # Find the closing </pre></div></div> sequence
    pre_start  = content.find('<pre', dot_start)
    pre_end    = content.find('</pre>', pre_start) + 6   # include </pre>
    close1     = content.find('</div>', pre_end)  + 6    # closes <pre> wrapper
    close2     = content.find('</div>', close1)   + 6    # closes bg-[#0a0e14] div

    new_block = (
        '<div class="bg-[#0a0e14] rounded-xl border border-outline-variant/20 '
        'overflow-hidden shadow-2xl">'
        '<div class="flex items-center gap-2 px-4 py-3 bg-surface-container-lowest '
        'border-b border-outline-variant/20">'
        '<span class="w-3 h-3 rounded-full bg-red-500 inline-block"></span>'
        '<span class="w-3 h-3 rounded-full bg-yellow-500 inline-block"></span>'
        '<span class="w-3 h-3 rounded-full bg-green-500 inline-block"></span>'
        f'<span class="ml-4 text-xs font-label text-slate-500 uppercase tracking-widest">'
        f'{html.escape(label)}</span>'
        '</div>'
        f'<pre class="code-block p-6 text-slate-300">{html.escape(sql, quote=False)}</pre>'
        '</div>'
    )

    content = content[:dot_start] + new_block + content[close2:]

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  ✅ {os.path.basename(os.path.dirname(path))}/code.html")


print("\n🔧 Replacing code blocks with clean plain-escaped SQL in all 14 files...\n")

for folder, (label, sql) in CODES.items():
    path = os.path.join(BASE, folder, "code.html")
    if not os.path.exists(path):
        print(f"  ❌ Not found: {path}")
        continue
    try:
        replace_code_block(path, label, sql)
    except Exception as e:
        print(f"  ❌ {folder}: {e}")

print("\n✅ All 14 code blocks replaced with clean plain-escaped SQL.\n")
