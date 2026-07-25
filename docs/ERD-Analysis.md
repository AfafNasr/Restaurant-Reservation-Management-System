# ERD Analysis

This document contains the analysis of the entities, attributes, relationships, keys, and cardinality before designing the Entity Relationship Diagram (ERD).

## Entities

### Restaurants
- `RestaurantId` (PK)
- `Name`
- `Address`
- `PhoneNumber`
- `OpeningHours`

### MenuItems
- `ItemId` (PK)
- `RestaurantId` (FK)
- `Name`
- `Description`
- `Price`

### Employees
- `EmployeeId` (PK)
- `RestaurantId` (FK)
- `FirstName`
- `LastName`
- `Position`

### Customers
- `CustomerId` (PK)
- `FirstName`
- `LastName`
- `Email`
- `PhoneNumber`

### Tables
- `TableId` (PK)
- `RestaurantId` (FK)
- `Capacity`

### Reservations
- `ReservationId` (PK)
- `CustomerId` (FK)
- `RestaurantId` (FK)
- `TableId` (FK)
- `ReservationDate`
- `PartySize`

### Orders
- `OrderId` (PK)
- `ReservationId` (FK)
- `EmployeeId` (FK)
- `OrderDate`
- `TotalAmount`

### OrderItems
- `OrderItemId` (PK)
- `OrderId` (FK)
- `ItemId` (FK)
- `Quantity`

## Relationships

- One restaurant has many menu items.
- One restaurant has many employees.
- One restaurant has many tables.
- One restaurant has many reservations.
- One customer has many reservations.
- One table has many reservations over time.
- One reservation has many orders.
- One employee can handle many orders.
- One order has many order items.
- One menu item can appear in many order items.