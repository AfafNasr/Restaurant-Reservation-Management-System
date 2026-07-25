USE RestaurantReservationDB;
GO

SELECT
    r.RestaurantId,
    r.Name AS RestaurantName,
    COUNT(res.ReservationId) AS ReservationCount,
    RANK() OVER (
        ORDER BY COUNT(res.ReservationId) DESC
    ) AS PopularityRank
FROM Restaurants AS r
LEFT JOIN Reservations AS res
    ON r.RestaurantId = res.RestaurantId
GROUP BY
    r.RestaurantId,
    r.Name
ORDER BY
    PopularityRank;
GO