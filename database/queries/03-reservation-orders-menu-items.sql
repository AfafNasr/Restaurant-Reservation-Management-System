USE RestaurantReservationDB;
GO

SELECT
    o.OrderId,
    o.ReservationId,
    o.OrderDate,
    mi.ItemId,
    mi.Name AS MenuItemName,
    oi.Quantity,
    mi.Price
FROM Orders AS o
INNER JOIN OrderItems AS oi
    ON oi.OrderId = o.OrderId
INNER JOIN MenuItems AS mi
    ON mi.ItemId = oi.ItemId
WHERE o.ReservationId = 1;
GO