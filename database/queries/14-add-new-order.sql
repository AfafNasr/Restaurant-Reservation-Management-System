USE RestaurantReservationDB;
GO

EXEC dbo.sp_AddNewOrder
    @ReservationId = 1,
    @EmployeeId = 1,
    @OrderDate = '2026-01-05 14:30:00',
    @TotalAmount = 85.00;
GO