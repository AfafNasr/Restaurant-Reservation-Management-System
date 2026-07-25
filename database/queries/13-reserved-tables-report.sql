USE RestaurantReservationDB;
GO

EXEC dbo.sp_ResrvedTablesReport
    @StartDate = '2026-01-01',
    @EndDate = '2026-01-31';
GO