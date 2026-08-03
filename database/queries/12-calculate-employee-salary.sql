USE RestaurantReservationDB;
GO

SELECT
    e.EmployeeId,
    e.FirstName,
    e.LastName,
    e.Position,
    dbo.fn_CalculateEmployeeSalary(e.EmployeeId) AS Salary
FROM dbo.Employees AS e
WHERE e.EmployeeId = 1;
GO