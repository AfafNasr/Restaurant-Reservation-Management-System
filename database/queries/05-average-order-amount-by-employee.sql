USE RestaurantReservationDB;
GO

SELECT
    AVG(TotalAmount) AS AverageOrderAmount
FROM Orders
WHERE EmployeeId = 1;
GO