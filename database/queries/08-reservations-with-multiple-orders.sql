USE RestaurantReservationDB;
GO

WITH ReservationOrderCounts AS
(
    SELECT
        ReservationId,
        COUNT(OrderId) AS OrderCount
    FROM dbo.Orders
    GROUP BY ReservationId
)
SELECT
    ReservationId,
    OrderCount
FROM dbo.ReservationOrderCounts
WHERE OrderCount >= 2;
GO

