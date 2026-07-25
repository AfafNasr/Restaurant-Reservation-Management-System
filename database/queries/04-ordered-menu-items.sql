USE RestaurantReservationDB;
GO

SELECT
    o.ReservationId,
    o.OrderId,
    mi.ItemId,
    mi.Name AS MenuItemName,
    mi.Description,
    mi.Price,
    oi.Quantity
FROM Orders AS o
INNER JOIN OrderItems AS oi
    ON oi.OrderId = o.OrderId
INNER JOIN MenuItems AS mi
    ON mi.ItemId = oi.ItemId
WHERE o.ReservationId = 1;
GO