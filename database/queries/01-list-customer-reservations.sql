USE RestaurantReservationDB;
GO

SELECT
    ReservationId,
    CustomerId,
    RestaurantId,
    TableId,
    ReservationDate,
    PartySize
FROM dbo.Reservations
WHERE CustomerId = 1;
GO