USE RestaurantReservationDB;
GO

CREATE PROCEDURE dbo.sp_FutureReservedTables
AS
BEGIN
    CREATE TABLE #FutureReservedTables
    (
        ReservationId INT,
        TableId INT,
        RestaurantId INT,
        ReservationDate DATETIME2,
        PartySize INT
    );

    INSERT INTO #FutureReservedTables
    (
        ReservationId,
        TableId,
        RestaurantId,
        ReservationDate,
        PartySize
    )
    SELECT
        r.ReservationId,
        r.TableId,
        r.RestaurantId,
        r.ReservationDate,
        r.PartySize
    FROM Reservations AS r
    WHERE r.ReservationDate > GETDATE();

    SELECT
        frt.ReservationId,
        frt.ReservationDate,
        frt.PartySize,

        t.TableId,
        t.Capacity,

        res.RestaurantId,
        res.Name AS RestaurantName,
        res.Address AS RestaurantAddress,
        res.PhoneNumber AS RestaurantPhoneNumber,
        res.OpeningHours
    FROM #FutureReservedTables AS frt
    INNER JOIN Tables AS t
        ON frt.TableId = t.TableId
    INNER JOIN Restaurants AS res
        ON frt.RestaurantId = res.RestaurantId
    ORDER BY frt.ReservationDate;
END;
GO