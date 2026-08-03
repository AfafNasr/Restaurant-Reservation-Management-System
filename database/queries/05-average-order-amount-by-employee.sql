USE RestaurantReservationDB;
GO

SELECT
    AVG(TotalAmount) AS AverageOrderAmount
FROM dbo.Orders
WHERE EmployeeId = 1;
GO