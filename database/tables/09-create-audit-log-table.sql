USE RestaurantReservationDB;
GO

CREATE TABLE dbo.AuditLog
(
    AuditLogId INT IDENTITY(1,1) PRIMARY KEY,
    RestaurantId INT NOT NULL,
    TableId INT NOT NULL,
    ReservationDate DATETIME2 NOT NULL,
    ChangeDate DATETIME2 NOT NULL
        CONSTRAINT DF_AuditLog_ChangeDate DEFAULT GETDATE()
);
GO