USE RestaurantReservationDB;
GO

CREATE FUNCTION dbo.fn_CalculateEmployeeSalary
(
    @EmployeeId INT
)
RETURNS INT
AS
BEGIN
    DECLARE @OrderCount INT;
    DECLARE @EmployeeRank INT;
    DECLARE @Salary INT;

    SELECT
        @OrderCount = COUNT(OrderId)
    FROM dbo.Orders
    WHERE EmployeeId = @EmployeeId;

    SELECT
        @EmployeeRank =
            CASE Position
                WHEN 'VIPOrdersWaiter' THEN 5
                WHEN 'StandardWaiter' THEN 4
                WHEN 'AssistantWaiter' THEN 3
                ELSE 0
            END
    FROM dbo.Employees
    WHERE EmployeeId = @EmployeeId;

    SET @Salary = @OrderCount * @EmployeeRank;

    RETURN @Salary;
END;
GO