CREATE DATABASE IF NOT EXISTS rrg;
USE rrg;

-- Create table for user information
CREATE TABLE IF NOT EXISTS UserInfo (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Username TEXT NOT NULL,
    Email TEXT NOT NULL,
    Password TEXT NOT NULL,
    UNIQUE (Username(255)), -- specifying a key length of 255 characters for Username
    UNIQUE (Email(255)) -- specifying a key length of 255 characters for Email
);

-- Create table for storing multiple passwords for each user
CREATE TABLE IF NOT EXISTS UserPasswords (
    PasswordID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    Password TEXT NOT NULL,
    FOREIGN KEY (UserID) REFERENCES UserInfo(UserID)
);
