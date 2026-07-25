USE RestaurantReservationDB;
GO

INSERT INTO dbo.Reservations
(
    CustomerId,
    RestaurantId,
    TableId,
    ReservationDate,
    PartySize
)
VALUES
(
    1,
    4,
    7,
    '2026-09-01 18:00:00',
    2
);
GO

SELECT
    AuditLogId,
    RestaurantId,
    TableId,
    ReservationDate,
    ChangeDate
FROM dbo.AuditLog
ORDER BY AuditLogId DESC;
GO