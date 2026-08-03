USE RestaurantReservationDB;
GO

CREATE FUNCTION dbo.fn_CalculateRevenue
(
    @RestaurantId INT
)
RETURNS DECIMAL(18, 2)
AS
BEGIN
    DECLARE @TotalRevenue DECIMAL(18, 2);

    SELECT
        @TotalRevenue = COALESCE(SUM(o.TotalAmount), 0)
    FROM dbo.Reservations AS r
    INNER JOIN dbo.Orders AS o
        ON r.ReservationId = o.ReservationId
    WHERE r.RestaurantId = @RestaurantId;

    RETURN @TotalRevenue;
END;
GO