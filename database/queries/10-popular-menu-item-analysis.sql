USE RestaurantReservationDB;
GO

WITH MenuItemPopularity AS
(
    SELECT
        r.RestaurantId,
        r.Name AS RestaurantName,
        mi.ItemId,
        mi.Name AS MenuItemName,
        SUM(oi.Quantity) AS TotalQuantityOrdered
    FROM dbo.Restaurants AS r
    INNER JOIN dbo.MenuItems AS mi
        ON r.RestaurantId = mi.RestaurantId
    INNER JOIN dbo.OrderItems AS oi
        ON mi.ItemId = oi.ItemId
    INNER JOIN dbo.Orders AS o
        ON oi.OrderId = o.OrderId
    WHERE o.OrderDate >= '2026-01-01'
      AND o.OrderDate <  '2026-02-01'
    GROUP BY
        r.RestaurantId,
        r.Name,
        mi.ItemId,
        mi.Name
),
RankedMenuItems AS
(
    SELECT
        RestaurantId,
        RestaurantName,
        ItemId,
        MenuItemName,
        TotalQuantityOrdered,
        RANK() OVER
        (
            PARTITION BY RestaurantId
            ORDER BY TotalQuantityOrdered DESC
        ) AS PopularityRank
    FROM dbo.MenuItemPopularity
)
SELECT
    RestaurantId,
    RestaurantName,
    ItemId,
    MenuItemName,
    TotalQuantityOrdered,
    PopularityRank
FROM dbo.RankedMenuItems
WHERE PopularityRank = 1
ORDER BY RestaurantId;
GO