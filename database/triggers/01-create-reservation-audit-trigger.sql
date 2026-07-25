USE RestaurantReservationDB;
GO

CREATE TRIGGER dbo.trg_LogTableReservation
ON dbo.Reservations
AFTER INSERT
AS
BEGIN
    INSERT INTO dbo.AuditLog
    (
        RestaurantId,
        TableId,
        ReservationDate,
        ChangeDate
    )
    SELECT
        i.RestaurantId,
        i.TableId,
        i.ReservationDate,
        GETDATE()
    FROM inserted AS i;
END;
GO