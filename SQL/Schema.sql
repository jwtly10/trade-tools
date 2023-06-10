CREATE DATABASE trade_tools_db;

CREATE TABLE trades_tb (
	ticketID INT NOT NULL,
    accountID INT NOT NULL, 
    tradeType VARCHAR(25) NOT NULL, 
    symbol VARCHAR(25) NOT NULL, 
    price DECIMAL (10,2) NOT NULL,
    sl DECIMAL(10,2),
    tp DECIMAL(10,2),
    swap DECIMAL(10,2), 
    profit DECIMAL(10,2), 
    created DATETIME NOT NULL, 
    closed DATETIME DEFAULT NULL,
    outcome VARCHAR(10) DEFAULT NULL,
    PRIMARY KEY(ticketID, accountID)
);
CREATE TABLE accounts_tb (
	accountID INT NOT NULL PRIMARY KEY,
    accountSize INT NOT NULL,
    accountState VARCHAR(30) NOT NULL,
    created datetime DEFAULT NOW() NOT NULL
);



