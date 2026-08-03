USE RestaurantReservationDB;
GO

SELECT
    r.RestaurantId,
    r.Name AS RestaurantName,
    dbo.fn_CalculateRevenue(r.RestaurantId) AS TotalRevenue
FROM dbo.Restaurants AS r
WHERE r.RestaurantId = 1;
GO