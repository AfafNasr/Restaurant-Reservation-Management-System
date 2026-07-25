USE RestaurantReservationDB;
GO

CREATE VIEW vw_ReservationsReport
AS
SELECT
    r.ReservationId,
    r.ReservationDate,
    r.PartySize,
    r.TableId,

    c.CustomerId,
    c.FirstName,
    c.LastName,
    c.Email,
    c.PhoneNumber,

    res.RestaurantId,
    res.Name AS RestaurantName,
    res.Address,
    res.PhoneNumber AS RestaurantPhoneNumber,
    res.OpeningHours
FROM Reservations AS r
INNER JOIN Customers AS c
    ON r.CustomerId = c.CustomerId
INNER JOIN Restaurants AS res
    ON r.RestaurantId = res.RestaurantId;
GO