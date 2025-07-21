# Task-Management-system
A command-line task and user management system built in Python using MySQL. Supports CRUD operations, task filtering, sorting, status transitions, and due date validation—all from your terminal!


FEATURES USED 

Create, view, update, and delete - Users

Create, view, update, and delete - Tasks

Filter tasks by status, priority, or date range

Sort tasks by due date or priority

Enforce status transitions (Pending → InProgress → Completed)

Validate due dates to prevent past deadlines

TECHNOLOGIES  :- Python, MySQL 

SQL CODE 

create database task_db;
use task_db;

CREATE TABLE User (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100),
    Email VARCHAR(100) UNIQUE
);

CREATE TABLE TaskItem (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    Title VARCHAR(100),
    Description TEXT,
    Status ENUM('Pending', 'InProgress', 'Completed') DEFAULT 'Pending',
    Priority ENUM('Low', 'Medium', 'High') DEFAULT 'Medium',
    DueDate DATETIME,
    UserId INT,
    FOREIGN KEY (UserId) REFERENCES User(Id)
);


