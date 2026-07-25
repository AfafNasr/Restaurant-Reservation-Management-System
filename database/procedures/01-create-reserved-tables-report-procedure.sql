USE RestaurantReservationDB;
GO

CREATE PROCEDURE dbo.sp_ResrvedTablesReport
    @StartDate DATETIME2,
    @EndDate DATETIME2
AS
BEGIN
    SELECT
        res.ReservationId,
        res.ReservationDate,
        res.PartySize,

        t.TableId,
        t.Capacity,

        r.RestaurantId,
        r.Name AS RestaurantName,
        r.Address AS RestaurantAddress,
        r.PhoneNumber AS RestaurantPhoneNumber
    FROM Reservations AS res
    INNER JOIN Tables AS t
        ON res.TableId = t.TableId
    INNER JOIN Restaurants AS r
        ON res.RestaurantId = r.RestaurantId
    WHERE res.ReservationDate >= @StartDate
      AND res.ReservationDate < DATEADD(DAY, 1, @EndDate)
    ORDER BY res.ReservationDate;
END;
GO