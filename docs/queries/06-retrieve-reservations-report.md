# Query 6: Retrieve Reservations Report Using a View

## Requirement

Retrieve Reservations Report with Views: Use a view to list all reservations information including restaurants and customers information.

## SQL Files

- [View Definition](../../database/views/01-create-reservations-report-view.sql)
- [Report Query](../../database/queries/06-retrieve-reservations-report.sql)

## Description

This query retrieves a complete reservations report from the `vw_ReservationsReport` view.

The view combines reservation information with the related customer and restaurant information. The report query then retrieves the combined data using a simple `SELECT` statement.

## Rationale

Reservation, customer, and restaurant information is stored in separate related tables. Therefore, the view uses `INNER JOIN` to combine:

- `Reservations`
- `Customers`
- `Restaurants`

The view stores the reusable query definition, while the report query retrieves its results. This avoids rewriting the joins whenever the reservations report is needed.

## Result

![Reservations Report Result](../query-results/06-retrieve-reservations-report.png)