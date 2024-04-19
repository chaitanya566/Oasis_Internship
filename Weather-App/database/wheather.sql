create database if not exists wheather;
use wheather;


-- Create table for user information
CREATE TABLE IF NOT EXISTS UserInfo (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Username TEXT NOT NULL,
    Email TEXT NOT NULL,
    Password TEXT NOT NULL,
    UNIQUE (Username(255)), 
    UNIQUE (Email(255)) 
);

-- Create table for user search history
CREATE TABLE IF NOT EXISTS SearchHistory (
    SearchID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    SearchQuery TEXT NOT NULL,
    SearchTimestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES UserInfo(UserID)
);
