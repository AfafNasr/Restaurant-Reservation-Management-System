USE RestaurantReservationDB;
GO

/* =========================================================
   1. Customer Reservations

   Used by:
   WHERE CustomerId = @CustomerId

   Supports retrieving all reservations for a specific
   customer without scanning the entire Reservations table.
   ========================================================= */

IF NOT EXISTS
(
    SELECT 1
    FROM sys.indexes
    WHERE name = 'IX_Reservations_CustomerId'
      AND object_id = OBJECT_ID('dbo.Reservations')
)
BEGIN
    CREATE NONCLUSTERED INDEX IX_Reservations_CustomerId
    ON dbo.Reservations (CustomerId)
    INCLUDE
    (
        RestaurantId,
        TableId,
        ReservationDate,
        PartySize
    );
END;
GO


/* =========================================================
   2. Reservations by Restaurant

   Used by:
   - vw_ReservationsReport
   - Restaurant popularity query
   - fn_CalculateRevenue
   - Joins between Reservations and Restaurants

   Supports grouping and joining reservations by restaurant.
   ========================================================= */

IF NOT EXISTS
(
    SELECT 1
    FROM sys.indexes
    WHERE name = 'IX_Reservations_RestaurantId'
      AND object_id = OBJECT_ID('dbo.Reservations')
)
BEGIN
    CREATE NONCLUSTERED INDEX IX_Reservations_RestaurantId
    ON dbo.Reservations (RestaurantId)
    INCLUDE
    (
        CustomerId,
        TableId,
        ReservationDate,
        PartySize
    );
END;
GO


/* =========================================================
   3. Reservations by Date

   Used by:
   - sp_ResrvedTablesReport
   - sp_FutureReservedTables

   Supports:
   ReservationDate >= @StartDate
   ReservationDate < @EndDate
   ReservationDate > GETDATE()
   ========================================================= */

IF NOT EXISTS
(
    SELECT 1
    FROM sys.indexes
    WHERE name = 'IX_Reservations_ReservationDate'
      AND object_id = OBJECT_ID('dbo.Reservations')
)
BEGIN
    CREATE NONCLUSTERED INDEX IX_Reservations_ReservationDate
    ON dbo.Reservations (ReservationDate)
    INCLUDE
    (
        RestaurantId,
        TableId,
        CustomerId,
        PartySize
    );
END;
GO


/* =========================================================
   4. Orders by Reservation

   Used by:
   - Orders and menu items query
   - Ordered menu items query
   - Reservations having two or more orders
   - fn_CalculateRevenue

   Supports filtering, joining, counting, and grouping orders
   using ReservationId.
   ========================================================= */

IF NOT EXISTS
(
    SELECT 1
    FROM sys.indexes
    WHERE name = 'IX_Orders_ReservationId'
      AND object_id = OBJECT_ID('dbo.Orders')
)
BEGIN
    CREATE NONCLUSTERED INDEX IX_Orders_ReservationId
    ON dbo.Orders (ReservationId)
    INCLUDE
    (
        EmployeeId,
        OrderDate,
        TotalAmount
    );
END;
GO


/* =========================================================
   5. Orders by Employee

   Used by:
   - Average order amount query
   - fn_CalculateEmployeeSalary

   Supports filtering and counting orders by EmployeeId.
   ========================================================= */

IF NOT EXISTS
(
    SELECT 1
    FROM sys.indexes
    WHERE name = 'IX_Orders_EmployeeId'
      AND object_id = OBJECT_ID('dbo.Orders')
)
BEGIN
    CREATE NONCLUSTERED INDEX IX_Orders_EmployeeId
    ON dbo.Orders (EmployeeId)
    INCLUDE
    (
        ReservationId,
        OrderDate,
        TotalAmount
    );
END;
GO


/* =========================================================
   6. Employees by Position

   Used by:
   WHERE Position = 'Manager'

   Supports retrieving employees according to their position.
   ========================================================= */

IF NOT EXISTS
(
    SELECT 1
    FROM sys.indexes
    WHERE name = 'IX_Employees_Position'
      AND object_id = OBJECT_ID('dbo.Employees')
)
BEGIN
    CREATE NONCLUSTERED INDEX IX_Employees_Position
    ON dbo.Employees (Position)
    INCLUDE
    (
        RestaurantId,
        FirstName,
        LastName
    );
END;
GO


/* =========================================================
   7. Order Items by Menu Item

   Used by:
   - Popular menu item analysis
   - SUM(Quantity) grouped by ItemId

   Supports joining OrderItems with MenuItems and calculating
   the total ordered quantity for each menu item.
   ========================================================= */

IF NOT EXISTS
(
    SELECT 1
    FROM sys.indexes
    WHERE name = 'IX_OrderItems_ItemId'
      AND object_id = OBJECT_ID('dbo.OrderItems')
)
BEGIN
    CREATE NONCLUSTERED INDEX IX_OrderItems_ItemId
    ON dbo.OrderItems (ItemId)
    INCLUDE
    (
        OrderId,
        Quantity
    );
END;
GO