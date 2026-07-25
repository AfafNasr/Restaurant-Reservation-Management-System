USE RestaurantReservationDB;
GO

CREATE VIEW vw_EmployeesReport
AS
SELECT
    e.EmployeeId,
    e.FirstName,
    e.LastName,
    e.Position,

    r.RestaurantId,
    r.Name AS RestaurantName,
    r.Address AS RestaurantAddress,
    r.PhoneNumber AS RestaurantPhoneNumber,
    r.OpeningHours
FROM Employees AS e
INNER JOIN Restaurants AS r
    ON e.RestaurantId = r.RestaurantId;
GO