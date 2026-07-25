CREATE DATABASE RestaurantReservationDB;
GO

USE RestaurantReservationDB;
GO

CREATE TABLE Restaurants
(
    RestaurantId INT IDENTITY(1,1) NOT NULL,
    Name NVARCHAR(100) NOT NULL,
    Address NVARCHAR(255) NOT NULL,
    PhoneNumber NVARCHAR(20) NOT NULL,
    OpeningHours NVARCHAR(100) NOT NULL,

    CONSTRAINT PK_Restaurants
        PRIMARY KEY (RestaurantId)
);
GO

CREATE TABLE Customers
(
    CustomerId INT IDENTITY(1,1) NOT NULL,
    FirstName NVARCHAR(50) NOT NULL,
    LastName NVARCHAR(50) NOT NULL,
    Email NVARCHAR(255) NOT NULL,
    PhoneNumber NVARCHAR(20) NOT NULL,

    CONSTRAINT PK_Customers
        PRIMARY KEY (CustomerId),

    CONSTRAINT UQ_Customers_Email
        UNIQUE (Email)
);
GO

CREATE TABLE Employees
(
    EmployeeId INT IDENTITY(1,1) NOT NULL,
    RestaurantId INT NOT NULL,
    FirstName NVARCHAR(50) NOT NULL,
    LastName NVARCHAR(50) NOT NULL,
    Position NVARCHAR(50) NOT NULL,

    CONSTRAINT PK_Employees
        PRIMARY KEY (EmployeeId),

    CONSTRAINT FK_Employees_Restaurants
        FOREIGN KEY (RestaurantId)
        REFERENCES Restaurants(RestaurantId)
);
GO

CREATE TABLE Tables
(
    TableId INT IDENTITY(1,1) NOT NULL,
    RestaurantId INT NOT NULL,
    Capacity INT NOT NULL,

    CONSTRAINT PK_Tables
        PRIMARY KEY (TableId),

    CONSTRAINT FK_Tables_Restaurants
        FOREIGN KEY (RestaurantId)
        REFERENCES Restaurants(RestaurantId),

    CONSTRAINT UQ_Tables_Restaurant_Table
        UNIQUE (RestaurantId, TableId),

    CONSTRAINT CHK_Tables_Capacity
        CHECK (Capacity > 0)
);
GO

CREATE TABLE MenuItems
(
    ItemId INT IDENTITY(1,1) NOT NULL,
    RestaurantId INT NOT NULL,
    Name NVARCHAR(100) NOT NULL,
    Description NVARCHAR(500) NULL,
    Price DECIMAL(10,2) NOT NULL,

    CONSTRAINT PK_MenuItems
        PRIMARY KEY (ItemId),

    CONSTRAINT FK_MenuItems_Restaurants
        FOREIGN KEY (RestaurantId)
        REFERENCES Restaurants(RestaurantId),

    CONSTRAINT CHK_MenuItems_Price
        CHECK (Price >= 0)
);
GO

CREATE TABLE Reservations
(
    ReservationId INT IDENTITY(1,1) NOT NULL,
    CustomerId INT NOT NULL,
    RestaurantId INT NOT NULL,
    TableId INT NOT NULL,
    ReservationDate DATETIME2 NOT NULL,
    PartySize INT NOT NULL,

    CONSTRAINT PK_Reservations
        PRIMARY KEY (ReservationId),

    CONSTRAINT FK_Reservations_Customers
        FOREIGN KEY (CustomerId)
        REFERENCES Customers(CustomerId),

    CONSTRAINT FK_Reservations_Tables
    FOREIGN KEY (RestaurantId, TableId)
    REFERENCES Tables(RestaurantId, TableId),

    CONSTRAINT CHK_Reservations_PartySize
        CHECK (PartySize > 0)
);
GO

CREATE TABLE Orders
(
    OrderId INT IDENTITY(1,1) NOT NULL,
    ReservationId INT NOT NULL,
    EmployeeId INT NOT NULL,
    OrderDate DATETIME2 NOT NULL
    CONSTRAINT DF_Orders_OrderDate DEFAULT (SYSDATETIME()),
    TotalAmount DECIMAL(10,2) NOT NULL
    CONSTRAINT DF_Orders_TotalAmount DEFAULT (0),

    CONSTRAINT PK_Orders
        PRIMARY KEY (OrderId),

    CONSTRAINT FK_Orders_Reservations
        FOREIGN KEY (ReservationId)
        REFERENCES Reservations(ReservationId),

    CONSTRAINT FK_Orders_Employees
        FOREIGN KEY (EmployeeId)
        REFERENCES Employees(EmployeeId),

    CONSTRAINT CHK_Orders_TotalAmount
        CHECK (TotalAmount >= 0)
);
GO

CREATE TABLE OrderItems
(
    OrderItemId INT IDENTITY(1,1) NOT NULL,
    OrderId INT NOT NULL,
    ItemId INT NOT NULL,
    Quantity INT NOT NULL,

    CONSTRAINT PK_OrderItems
        PRIMARY KEY (OrderItemId),

    CONSTRAINT FK_OrderItems_Orders
        FOREIGN KEY (OrderId)
        REFERENCES Orders(OrderId),

    CONSTRAINT FK_OrderItems_MenuItems
        FOREIGN KEY (ItemId)
        REFERENCES MenuItems(ItemId),

    CONSTRAINT CHK_OrderItems_Quantity
        CHECK (Quantity > 0),

    CONSTRAINT UQ_OrderItems_Order_Item
        UNIQUE (OrderId, ItemId)
);
GO
