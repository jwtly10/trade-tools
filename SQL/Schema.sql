CREATE DATABASE trade_tools_db;

CREATE TABLE trades (
	ticketID INT NOT NULL,
    accountID INT NOT NULL, 
    tradeType VARCHAR(25) NOT NULL, 
    symbol VARCHAR(25) NOT NULL, 
    price DECIMAL (10,2) NOT NULL,
    sl DECIMAL(10,2),
    tp DECIMAL(10,2),
    swap DECIMAL(10,2), 
    profit DECIMAL(10,2), 
    closed DATETIME,
    created DATETIME NOT NULL, 
    outcome VARCHAR(10),
    PRIMARY KEY(ticketID, accountID)
);



