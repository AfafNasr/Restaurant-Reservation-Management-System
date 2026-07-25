USE RestaurantReservationDB;
GO

SELECT
    EmployeeId,
    RestaurantId,
    FirstName,
    LastName,
    Position
FROM Employees
WHERE Position = 'Manager';
GO