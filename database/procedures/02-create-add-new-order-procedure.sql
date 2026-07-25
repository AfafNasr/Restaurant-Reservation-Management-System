USE RestaurantReservationDB;
GO

CREATE PROCEDURE dbo.sp_AddNewOrder
    @ReservationId INT,
    @EmployeeId INT,
    @OrderDate DATETIME2,
    @TotalAmount DECIMAL(18, 2)
AS
BEGIN
    IF NOT EXISTS
    (
        SELECT 1
        FROM Reservations
        WHERE ReservationId = @ReservationId
    )
    BEGIN
        THROW 50001, 'The specified reservation does not exist.', 1;
    END;

    IF NOT EXISTS
    (
        SELECT 1
        FROM Employees
        WHERE EmployeeId = @EmployeeId
    )
    BEGIN
        THROW 50002, 'The specified employee does not exist.', 1;
    END;

    INSERT INTO Orders
    (
        ReservationId,
        EmployeeId,
        OrderDate,
        TotalAmount
    )
    VALUES
    (
        @ReservationId,
        @EmployeeId,
        @OrderDate,
        @TotalAmount
    );

    DECLARE @NewOrderId INT;

    SET @NewOrderId = CAST(SCOPE_IDENTITY() AS INT);

    SELECT
       o.OrderId,
       o.ReservationId,
       o.EmployeeId,
       o.OrderDate,
       o.TotalAmount
   FROM Orders AS o
   WHERE o.OrderId = @NewOrderId;
   END;
GO