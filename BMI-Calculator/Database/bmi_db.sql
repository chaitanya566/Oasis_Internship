-- Table for user authentication information
create database if not exists BMI_db;
use BMI_db;
CREATE TABLE Users (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(50) NOT NULL,
    Email VARCHAR(100) NOT NULL,
    Password VARCHAR(100) NOT NULL
);

-- Table for storing BMI values for each user
CREATE TABLE BMIRecords (
    RecordID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT,
    Height FLOAT NOT NULL,
    Weight FLOAT NOT NULL,
    BMIScore FLOAT NOT NULL,
    DateRecorded DATE NOT NULL,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);
select * from Users;