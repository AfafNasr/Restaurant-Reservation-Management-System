USE RestaurantReservationDB;
GO

WITH ReservationOrderCounts AS
(
    SELECT
        ReservationId,
        COUNT(OrderId) AS OrderCount
    FROM Orders
    GROUP BY ReservationId
)
SELECT
    ReservationId,
    OrderCount
FROM ReservationOrderCounts
WHERE OrderCount >= 2;
GO

