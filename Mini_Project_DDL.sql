-- create database DalalBros
USE DalalBros;


CREATE TABLE Market (
    Mid INT PRIMARY KEY,
    name VARCHAR(50)
);

INSERT INTO Market VALUES (1, 'NYSE');
INSERT INTO Market VALUES (2, 'NASDAQ');
INSERT INTO Market VALUES (3, 'BSE');
INSERT INTO Market VALUES (4, 'LSE');
INSERT INTO Market VALUES (5, 'JPX');

CREATE TABLE Company (
    Company_id INT PRIMARY KEY,
    Name VARCHAR(50),
    Sector VARCHAR(50),
    Headquarters VARCHAR(50)
);

INSERT INTO Company VALUES 
(1, 'Apple', 'Technology', 'Cupertino'),
(2, 'Google', 'Technology', 'Mountain View'),
(3, 'Reliance', 'Conglomerate', 'Mumbai'),
(4, 'Toyota', 'Automobile', 'Toyota City'),
(5, 'Shell', 'Energy', 'London');

CREATE TABLE Stock (
    stock_id INT PRIMARY KEY,
    ListingPrice DECIMAL(10,2),
    CurrentPrice DECIMAL(10,2),
    C_id INT,
    Mid INT,
    FOREIGN KEY (C_id) REFERENCES Company(Company_id),
    FOREIGN KEY (Mid) REFERENCES Market(Mid)
);


INSERT INTO Stock VALUES 
(100, 150.00, 155.25, 1, 1),
(101, 120.00, 118.80, 2, 2),
(102, 2100.00, 2105.50, 3, 3),
(103, 180.90, 179.25, 4, 4),
(104, 55.00, 57.35, 5, 5);

CREATE TABLE Portfolio (
    P_id INT PRIMARY KEY,
    PortfolioValue DECIMAL(12,2)
);

Alter table Portfolio
modify column PortfolioValue DECIMAL(12,2) NOT null;

INSERT INTO Portfolio VALUES 
(201, 100000.00),
(202, 54000.50),
(203, 82000.75),
(204, 167000.00),
(205, 47000.10);

CREATE TABLE Contains (
    P_id INT,
    Stock_id INT,
    PRIMARY KEY (P_id, Stock_id),
    FOREIGN KEY (P_id) REFERENCES Portfolio(P_id),
    FOREIGN KEY (Stock_id) REFERENCES Stock(stock_id)
);

INSERT INTO Contains VALUES 
(201, 100),
(202, 101),
(203, 102),
(204, 103),
(205, 104);

CREATE TABLE TradeOrder (
    Order_id INT PRIMARY KEY,
    Order_type VARCHAR(20),
    Quantity INT,
    S_id INT,
    P_id INT,
    FOREIGN KEY (S_id) REFERENCES Stock(stock_id),
    FOREIGN KEY (P_id) REFERENCES Portfolio(P_id)
);

alter table TradeOrder
modify column Quantity INT NOT NULL;

INSERT INTO TradeOrder VALUES 
(301, 'Buy', 50, 100, 201),
(302, 'Sell', 30, 101, 202),
(303, 'Buy', 100, 102, 203),
(304, 'Sell', 25, 103, 204),
(305, 'Buy', 75, 104, 205);

CREATE TABLE Transaction (
    T_id INT PRIMARY KEY,
    TradeType VARCHAR(20),
    Quantity INT,
    Price DECIMAL(10,2),
    Timestamp DATETIME
);

INSERT INTO Transaction VALUES 
(401, 'Buy', 25, 152.50, '2025-09-18 12:00:00'),
(402, 'Sell', 10, 117.90, '2025-09-18 12:10:00'),
(403, 'Buy', 50, 2103.00, '2025-09-18 12:20:00'),
(404, 'Sell', 20, 180.10, '2025-09-18 12:30:00'),
(405, 'Buy', 40, 56.80, '2025-09-18 12:40:00');

CREATE TABLE Broker (
    Broker_id INT PRIMARY KEY,
    License_no VARCHAR(30),
    Name VARCHAR(50),
    T_id INT,
    FOREIGN KEY (T_id) REFERENCES Transaction(T_id)
);

INSERT INTO Broker (Broker_id, License_no, Name) VALUES 
(11, 'LIC1234', 'ACME Brokers'),
(12, 'LIC5678', 'Prime Trade'),
(13, 'LIC9101', 'Broker Hub'),
(14, 'LIC1213', 'Global Equities'),
(15, 'LIC1415', 'Future Secure');

CREATE TABLE Investor (
    I_id INT PRIMARY KEY,
    Email VARCHAR(50),
    Balance DECIMAL(10,2),
    T_id INT,
    FOREIGN KEY (T_id) REFERENCES Transaction(T_id)
);

INSERT INTO Investor (I_id, Email, Balance) VALUES 
(101, 'alice@email.com', 10000.50),
(102, 'bob@email.com', 5000.00),
(103, 'carol@email.com', 15250.20),
(104, 'dave@email.com', 23000.00),
(105, 'eve@email.com', 7800.75);


CREATE TABLE RegisteredWith (
    B_id INT,
    I_id INT,
    PRIMARY KEY (B_id, I_id),
    FOREIGN KEY (B_id) REFERENCES Broker(Broker_id),
    FOREIGN KEY (I_id) REFERENCES Investor(I_id)
);

INSERT INTO RegisteredWith VALUES 
(11, 101),
(12, 102),
(13, 103),
(14, 104),
(15, 105);

CREATE TABLE Phone (
    I_id INT PRIMARY KEY,
    Phone_number VARCHAR(15),
    FOREIGN KEY (I_id) REFERENCES Investor(I_id)
);

DROP TABLE IF EXISTS Phone;
CREATE TABLE Phone (
    I_id INT,
    Phone_number VARCHAR(15),
    FOREIGN KEY (I_id) REFERENCES Investor(I_id),
    PRIMARY KEY (I_id, Phone_number)
);


INSERT INTO Phone VALUES 
(101, '1234567890'),
(102, '2345678901'),
(103, '3456789012'),
(104, '4567890123'),
(105, '5678901234');

	
ALTER TABLE Investor
ADD COLUMN Referrer_id INT,
ADD CONSTRAINT FK_Referrer
FOREIGN KEY (Referrer_id) REFERENCES Investor(I_id);

select * from Investor
    
    
UPDATE Investor SET Referrer_id = NULL WHERE I_id = 101; -- Alice has no referrer
UPDATE Investor SET Referrer_id = 101 WHERE I_id = 102;  -- Alice refers Bob
UPDATE Investor SET Referrer_id = 101 WHERE I_id = 104;  -- Alice refers Dave
UPDATE Investor SET Referrer_id = 102 WHERE I_id = 103;  -- Bob refers Carol
UPDATE Investor SET Referrer_id = 103 WHERE I_id = 105;  -- Carol refers Eve

-- Constraints
ALTER TABLE Market
MODIFY COLUMN name VARCHAR(50) NOT NULL,      -- Name must be present
ADD CONSTRAINT unique_market_name UNIQUE (name); -- No two markets have the same name

    
ALTER TABLE Company
MODIFY COLUMN Name VARCHAR(50) NOT NULL,
MODIFY COLUMN Headquarters VARCHAR(50) NOT NULL,
ADD CONSTRAINT unique_company_name UNIQUE (Name),
ADD CONSTRAINT check_sector CHECK (Sector IN ('Technology', 'Conglomerate', 'Automobile', 'Energy', 'Finance', 'Other'));

ALTER TABLE Stock
MODIFY COLUMN ListingPrice DECIMAL(10,2) NOT NULL,
MODIFY COLUMN CurrentPrice DECIMAL(10,2) NOT NULL,
ADD CONSTRAINT check_positive_listing CHECK (ListingPrice > 0),
ADD CONSTRAINT check_positive_current CHECK (CurrentPrice > 0),
ADD CONSTRAINT unique_per_company_stock UNIQUE(C_id, Mid); -- A company can't be listed twice on same market

ALTER TABLE Portfolio
MODIFY COLUMN PortfolioValue DECIMAL(12,2) NOT NULL DEFAULT 0,
ADD CONSTRAINT check_nonnegative_portfoliovalue CHECK (PortfolioValue >= 0);

ALTER TABLE TradeOrder
MODIFY COLUMN Quantity INT NOT NULL,
MODIFY COLUMN Order_type VARCHAR(20) NOT NULL,
ADD CONSTRAINT check_order_type_valid CHECK (Order_type IN ('Buy', 'Sell')),
ADD CONSTRAINT check_quantity_positive CHECK (Quantity > 0);

ALTER TABLE Transaction
MODIFY COLUMN Price DECIMAL(10,2) NOT NULL,
MODIFY COLUMN TradeType VARCHAR(20) NOT NULL,
ADD CONSTRAINT check_price_positive CHECK (Price > 0),
ADD CONSTRAINT check_valid_tradetype CHECK (TradeType IN ('Buy', 'Sell', 'Dividend', 'Bonus'));

ALTER TABLE Broker
MODIFY COLUMN License_no VARCHAR(30) NOT NULL,
ADD CONSTRAINT unique_license UNIQUE (License_no);

ALTER TABLE Investor
MODIFY COLUMN Email VARCHAR(50) NOT NULL,
ADD CONSTRAINT unique_email UNIQUE (Email),
ADD CONSTRAINT check_balance_nonnegative CHECK (Balance >= 0);

-- Triggers

-- Every time a portfolio is created, an audit record goes into AuditPortfolio
CREATE TABLE IF NOT EXISTS AuditPortfolio (
    AuditId INT AUTO_INCREMENT PRIMARY KEY,
    P_id INT,
    EventType VARCHAR(20),
    EventTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DELIMITER $$
CREATE TRIGGER LogPortfolioInsert
AFTER INSERT ON Portfolio
FOR EACH ROW
BEGIN
    INSERT INTO AuditPortfolio (P_id, EventType)
    VALUES (NEW.P_id, 'PORTFOLIO_CREATED');
END$$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER BlockNegativeBalance
BEFORE UPDATE ON Investor
FOR EACH ROW
BEGIN
    IF NEW.Balance < 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Investor balance cannot be negative';
    END IF;
END$$
DELIMITER ;

-- Functions

-- Returns the total shares held by a portfolio.
DELIMITER $$
CREATE FUNCTION PortfolioTotalHoldings(pid INT)
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE holdings INT;
    SELECT SUM(Quantity) INTO holdings
      FROM Contains WHERE P_id = pid;
    RETURN IFNULL(holdings,0);
END$$
DELIMITER ;

-- Counts total portfolios owned by a specific investor.
DELIMITER $$
CREATE FUNCTION InvestorPortfolioCount(inv_id INT)
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE countp INT;
    SELECT COUNT(*) INTO countp
      FROM Portfolio WHERE I_id = inv_id;
    RETURN countp;
END$$
DELIMITER ;

-- Procedures

-- Raises every stock’s price by a given percent.
DELIMITER $$
CREATE PROCEDURE IncreaseAllStockPricesBy(percent DECIMAL(5,2))
BEGIN
    UPDATE Stock
    SET CurrentPrice = CurrentPrice * (1 + percent/100);
END$$
DELIMITER ;

-- Sets a specific portfolio’s value to zero 
DELIMITER $$
CREATE PROCEDURE ResetPortfolioValue(pid INT)
BEGIN
    UPDATE Portfolio SET PortfolioValue = 0 WHERE P_id = pid;
END$$
DELIMITER ;


INSERT INTO Portfolio (P_id, PortfolioValue)
VALUES (206, 75000.00);

UPDATE Investor
SET Balance = -500
WHERE I_id = 102;

SELECT PortfolioTotalHoldings(201);

SELECT P_id, PortfolioTotalHoldings(P_id) AS TotalHoldings
FROM Portfolio;





ALTER TABLE Contains
ADD COLUMN Quantity INT NOT NULL DEFAULT 0;

UPDATE Contains SET Quantity = 50 WHERE P_id = 201 AND Stock_id = 100;
UPDATE Contains SET Quantity = 30 WHERE P_id = 202 AND Stock_id = 101;
UPDATE Contains SET Quantity = 80 WHERE P_id = 203 AND Stock_id = 102;
UPDATE Contains SET Quantity = 25 WHERE P_id = 204 AND Stock_id = 103;
UPDATE Contains SET Quantity = 100 WHERE P_id = 205 AND Stock_id = 104;


CALL IncreaseAllStockPricesBy(10);
CALL ResetPortfolioValue(201);



SET SQL_SAFE_UPDATES = 0;
CALL IncreaseAllStockPricesBy(100);
SET SQL_SAFE_UPDATES = 1;

desc RegisteredWith 
    
    
    
    
    
select CurrentPrice from Stock

    
    
    
    
    
    


    
    
    
    
    




    
    
    
    
    
    
    
    
    
    
    
    

    
    
    
    
    
    
    
   



