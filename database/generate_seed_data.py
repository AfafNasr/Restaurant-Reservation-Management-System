from __future__ import annotations

import random
from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Iterable, Sequence

# Produces the same data every time.
RANDOM_SEED = 42
OUTPUT_FILE = Path(__file__).with_name("02-seed-data.sql")

COUNTS = {
    "Restaurants": 50,
    "Customers": 400,
    "Employees": 100,
    "Tables": 100,
    "MenuItems": 1000,
    "Reservations": 500,
    "Orders": 500,
    "OrderItems": 1500,
}

MAX_ROWS_PER_INSERT = 500


@dataclass(frozen=True)
class Restaurant:
    restaurant_id: int
    name: str
    address: str
    phone_number: str
    opening_hours: str


@dataclass(frozen=True)
class Customer:
    customer_id: int
    first_name: str
    last_name: str
    email: str
    phone_number: str


@dataclass(frozen=True)
class Employee:
    employee_id: int
    restaurant_id: int
    first_name: str
    last_name: str
    position: str


@dataclass(frozen=True)
class DiningTable:
    table_id: int
    restaurant_id: int
    capacity: int


@dataclass(frozen=True)
class MenuItem:
    item_id: int
    restaurant_id: int
    name: str
    description: str
    price: Decimal


@dataclass(frozen=True)
class Reservation:
    reservation_id: int
    customer_id: int
    restaurant_id: int
    table_id: int
    reservation_date: datetime
    party_size: int


@dataclass(frozen=True)
class Order:
    order_id: int
    reservation_id: int
    employee_id: int
    order_date: datetime
    total_amount: Decimal


@dataclass(frozen=True)
class OrderItem:
    order_item_id: int
    order_id: int
    item_id: int
    quantity: int


def sql_string(value: str | None) -> str:
    if value is None:
        return "NULL"
    return "N'" + value.replace("'", "''") + "'"


def sql_datetime(value: datetime) -> str:
    return f"'{value:%Y-%m-%dT%H:%M:%S}'"


def sql_decimal(value: Decimal) -> str:
    return f"{value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP):.2f}"


def chunks(rows: Sequence[tuple[str, ...]], size: int) -> Iterable[Sequence[tuple[str, ...]]]:
    for start in range(0, len(rows), size):
        yield rows[start:start + size]


def build_insert(table: str, columns: Sequence[str], rows: Sequence[tuple[str, ...]]) -> str:
    statements: list[str] = []
    for batch in chunks(rows, MAX_ROWS_PER_INSERT):
        values = ",\n".join("    (" + ", ".join(row) + ")" for row in batch)
        statements.append(
            f"INSERT INTO {table} ({', '.join(columns)})\nVALUES\n{values};\nGO"
        )
    return "\n\n".join(statements)


def generate_restaurants() -> list[Restaurant]:
    restaurant_names = [
        "Olive & Thyme", "Cedar House", "Golden Spoon", "Urban Plate",
        "Garden Grill", "Sunset Kitchen", "Old City Table", "Sea Breeze",
        "Harvest Corner", "Royal Terrace",
    ]
    cities = [
        "Ramallah", "Nablus", "Bethlehem", "Hebron", "Jenin",
        "Tulkarm", "Jericho", "Qalqilya", "Gaza", "Rafah",
    ]
    streets = [
        "Al-Masyoun Street", "Rafidia Street", "Manger Street", "Ein Sara Street",
        "Haifa Street", "Nablus Street", "Hisham Palace Road", "Main Market Street",
        "Al-Rimal Street", "Sea Road",
    ]
    hours = [
        "08:00 AM - 10:00 PM",
        "09:00 AM - 11:00 PM",
        "10:00 AM - 12:00 AM",
    ]

    restaurants: list[Restaurant] = []
    for i in range(1, 51):
        idx = (i - 1) % 10
        restaurants.append(
            Restaurant(
                restaurant_id=i,
                name=f"{restaurant_names[idx]} {i}",
                address=f"{cities[idx]} - {streets[idx]}, Building {i}",
                phone_number=f"02{9500000 + i:07d}",
                opening_hours=hours[(i - 1) % len(hours)],
            )
        )
    return restaurants


def generate_customers() -> list[Customer]:
    first_names = [
        "Ahmad", "Mohammad", "Omar", "Yousef", "Ali", "Khaled", "Mahmoud", "Sami",
        "Lina", "Sara", "Noor", "Mariam", "Aya", "Hala", "Rana", "Dina",
        "Adam", "Tariq", "Rami", "Salma",
    ]
    last_names = [
        "Naser", "Khalil", "Haddad", "Saleh", "Mansour", "Hamdan", "Abu Ali",
        "Darwish", "Qasem", "Sabbagh", "Awad", "Shahin", "Barakat", "Jaber",
        "Masri", "Zaid", "Najjar", "Tamimi", "Suleiman", "Khatib",
    ]

    customers: list[Customer] = []
    for i in range(1, 401):
        first = first_names[(i - 1) % len(first_names)]
        last = last_names[((i - 1) * 7) % len(last_names)]
        customers.append(
            Customer(
                customer_id=i,
                first_name=first,
                last_name=last,
                email=f"{first.lower().replace(' ', '')}.{last.lower().replace(' ', '')}{i}@example.com",
                phone_number=f"059{1000000 + i:07d}",
            )
        )
    return customers


def generate_employees() -> list[Employee]:
    first_names = [
        "Amir", "Basil", "Fadi", "Hani", "Iyad", "Jamal", "Kareem", "Laith",
        "Maya", "Nadia", "Ruba", "Sahar", "Yara", "Zain", "Farah", "Dana",
    ]
    last_names = [
        "Abbas", "Hussein", "Ismail", "Kanaan", "Nimer", "Odeh", "Radi", "Saad",
        "Taha", "Yasin", "Zaki", "Bishara", "Daoud", "Elias", "Khoury", "Musa",
    ]

    waiter_positions = (
        "VIPOrdersWaiter",
        "StandardWaiter",
        "AssistantWaiter",
    )

    employees: list[Employee] = []
    employee_id = 1

    for restaurant_id in range(1, 51):
        positions = (
            "Manager",
            waiter_positions[(restaurant_id - 1) % len(waiter_positions)],
        )

        for position in positions:
            idx = employee_id - 1

            employees.append(
                Employee(
                    employee_id=employee_id,
                    restaurant_id=restaurant_id,
                    first_name=first_names[idx % len(first_names)],
                    last_name=last_names[(idx * 5) % len(last_names)],
                    position=position,
                )
            )

            employee_id += 1

    return employees


def generate_tables() -> list[DiningTable]:
    dining_tables: list[DiningTable] = []
    table_id = 1
    for restaurant_id in range(1, 51):
        dining_tables.append(DiningTable(table_id, restaurant_id, 4))
        table_id += 1
        dining_tables.append(DiningTable(table_id, restaurant_id, 6))
        table_id += 1
    return dining_tables


def generate_menu_items() -> list[MenuItem]:
    templates = [
        ("Lentil Soup", "Warm lentil soup with cumin and lemon", "5.50"),
        ("Fattoush Salad", "Fresh vegetables, toasted bread, and sumac dressing", "7.00"),
        ("Hummus Plate", "Creamy chickpea dip served with olive oil", "6.00"),
        ("Baba Ghanoush", "Smoked eggplant dip with tahini", "6.50"),
        ("Falafel Platter", "Falafel served with salad, pickles, and tahini", "8.50"),
        ("Chicken Shawarma", "Marinated chicken with garlic sauce and vegetables", "12.00"),
        ("Beef Shawarma", "Seasoned beef with tahini and vegetables", "13.50"),
        ("Grilled Chicken", "Char-grilled chicken breast with seasonal vegetables", "15.00"),
        ("Mixed Grill", "Assortment of kebab, chicken, and lamb", "22.00"),
        ("Kofta Kebab", "Grilled minced meat skewers with herbs", "16.00"),
        ("Mansaf", "Lamb with rice and traditional yogurt sauce", "20.00"),
        ("Maqluba", "Layered rice dish with chicken and vegetables", "17.50"),
        ("Musakhan", "Roasted chicken with sumac onions on taboon bread", "18.00"),
        ("Seafood Pasta", "Pasta with shrimp and creamy herb sauce", "19.00"),
        ("Margherita Pizza", "Tomato, mozzarella, and basil", "13.00"),
        ("Vegetable Pizza", "Seasonal vegetables, tomato, and mozzarella", "14.00"),
        ("Cheesecake", "Classic baked cheesecake with berry sauce", "7.50"),
        ("Kunafa", "Sweet cheese pastry with syrup and pistachios", "8.00"),
        ("Fresh Lemonade", "Fresh lemon juice with mint", "4.00"),
        ("Arabic Coffee", "Traditional cardamom coffee", "3.50"),
    ]

    menu_items: list[MenuItem] = []
    item_id = 1
    for restaurant_id in range(1, 51):
        price_adjustment = Decimal((restaurant_id - 1) % 5) * Decimal("0.25")
        for name, description, base_price in templates:
            menu_items.append(
                MenuItem(
                    item_id=item_id,
                    restaurant_id=restaurant_id,
                    name=name,
                    description=description,
                    price=Decimal(base_price) + price_adjustment,
                )
            )
            item_id += 1
    return menu_items


def generate_reservations(
    rng: random.Random,
    dining_tables: list[DiningTable],
) -> list[Reservation]:
    tables_by_restaurant: dict[int, list[DiningTable]] = {}
    for table in dining_tables:
        tables_by_restaurant.setdefault(table.restaurant_id, []).append(table)

    reservations: list[Reservation] = []
    reservation_id = 1
    base_date = datetime(2026, 1, 5, 12, 0, 0)
    available_hours = [12, 14, 17, 19, 21]

    for restaurant_id in range(1, 51):
        restaurant_tables = tables_by_restaurant[restaurant_id]
        for local_index in range(10):
            table = restaurant_tables[local_index % len(restaurant_tables)]
            day_offset = (restaurant_id - 1) * 3 + local_index
            reservation_date = base_date + timedelta(days=day_offset)
            reservation_date = reservation_date.replace(
                hour=available_hours[local_index % len(available_hours)],
                minute=30 if local_index % 2 else 0,
            )
            party_size = rng.randint(1, table.capacity)
            customer_id = ((reservation_id - 1) % 400) + 1

            reservations.append(
                Reservation(
                    reservation_id=reservation_id,
                    customer_id=customer_id,
                    restaurant_id=restaurant_id,
                    table_id=table.table_id,
                    reservation_date=reservation_date,
                    party_size=party_size,
                )
            )
            reservation_id += 1

    return reservations


def generate_orders_and_items(
    rng: random.Random,
    reservations: list[Reservation],
    employees: list[Employee],
    menu_items: list[MenuItem],
) -> tuple[list[Order], list[OrderItem]]:
    employees_by_restaurant: dict[int, list[Employee]] = {}
    for employee in employees:
        employees_by_restaurant.setdefault(employee.restaurant_id, []).append(employee)

    menu_by_restaurant: dict[int, list[MenuItem]] = {}
    menu_by_id: dict[int, MenuItem] = {}
    for item in menu_items:
        menu_by_restaurant.setdefault(item.restaurant_id, []).append(item)
        menu_by_id[item.item_id] = item

    orders: list[Order] = []
    order_items: list[OrderItem] = []
    order_item_id = 1

    for reservation in reservations:
        order_id = reservation.reservation_id
        restaurant_employees = employees_by_restaurant[reservation.restaurant_id]
        # Prefer the server while still using both employees across the data.
        employee = restaurant_employees[order_id % len(restaurant_employees)]

        restaurant_menu = menu_by_restaurant[reservation.restaurant_id]
        selected_items = rng.sample(restaurant_menu, 3)

        total = Decimal("0.00")
        pending_items: list[OrderItem] = []

        for selected in selected_items:
            quantity = rng.randint(1, 4)
            pending_items.append(
                OrderItem(
                    order_item_id=order_item_id,
                    order_id=order_id,
                    item_id=selected.item_id,
                    quantity=quantity,
                )
            )
            order_item_id += 1
            total += selected.price * quantity

        order_date = reservation.reservation_date + timedelta(minutes=rng.choice([30, 45, 60, 75, 90]))
        orders.append(
            Order(
                order_id=order_id,
                reservation_id=reservation.reservation_id,
                employee_id=employee.employee_id,
                order_date=order_date,
                total_amount=total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            )
        )
        order_items.extend(pending_items)

    return orders, order_items


def validate_data(
    restaurants: list[Restaurant],
    customers: list[Customer],
    employees: list[Employee],
    dining_tables: list[DiningTable],
    menu_items: list[MenuItem],
    reservations: list[Reservation],
    orders: list[Order],
    order_items: list[OrderItem],
) -> None:
    actual_counts = {
        "Restaurants": len(restaurants),
        "Customers": len(customers),
        "Employees": len(employees),
        "Tables": len(dining_tables),
        "MenuItems": len(menu_items),
        "Reservations": len(reservations),
        "Orders": len(orders),
        "OrderItems": len(order_items),
    }
    if actual_counts != COUNTS:
        raise ValueError(f"Incorrect generated counts: {actual_counts}")

    restaurant_ids = {r.restaurant_id for r in restaurants}
    customer_ids = {c.customer_id for c in customers}
    emails = [c.email for c in customers]
    if len(emails) != len(set(emails)):
        raise ValueError("Customer emails must be unique.")

    table_by_id = {t.table_id: t for t in dining_tables}
    employee_by_id = {e.employee_id: e for e in employees}
    menu_by_id = {m.item_id: m for m in menu_items}
    reservation_by_id = {r.reservation_id: r for r in reservations}
    order_by_id = {o.order_id: o for o in orders}

    for employee in employees:
        if employee.restaurant_id not in restaurant_ids:
            raise ValueError("Employee references a missing restaurant.")

    for table in dining_tables:
        if table.restaurant_id not in restaurant_ids or table.capacity <= 0:
            raise ValueError("Invalid dining table.")

    for item in menu_items:
        if item.restaurant_id not in restaurant_ids or item.price < 0:
            raise ValueError("Invalid menu item.")

    for reservation in reservations:
        if reservation.customer_id not in customer_ids:
            raise ValueError("Reservation references a missing customer.")
        table = table_by_id[reservation.table_id]
        if table.restaurant_id != reservation.restaurant_id:
            raise ValueError("Reservation table belongs to another restaurant.")
        if not 1 <= reservation.party_size <= table.capacity:
            raise ValueError("Reservation party size exceeds table capacity.")

    seen_order_reservations: set[int] = set()
    for order in orders:
        reservation = reservation_by_id[order.reservation_id]
        employee = employee_by_id[order.employee_id]
        if employee.restaurant_id != reservation.restaurant_id:
            raise ValueError("Order employee belongs to another restaurant.")
        if order.reservation_id in seen_order_reservations:
            raise ValueError("More than one order was generated for a reservation.")
        seen_order_reservations.add(order.reservation_id)

    items_by_order: dict[int, list[OrderItem]] = {}
    for order_item in order_items:
        items_by_order.setdefault(order_item.order_id, []).append(order_item)

    for order_id, items in items_by_order.items():
        if len(items) != 3:
            raise ValueError("Every order must contain exactly three order items.")
        if len({item.item_id for item in items}) != 3:
            raise ValueError("An item is duplicated inside an order.")

        order = order_by_id[order_id]
        reservation = reservation_by_id[order.reservation_id]
        calculated_total = Decimal("0.00")

        for order_item in items:
            if order_item.quantity <= 0:
                raise ValueError("Order item quantity must be positive.")
            menu_item = menu_by_id[order_item.item_id]
            if menu_item.restaurant_id != reservation.restaurant_id:
                raise ValueError("Order item belongs to another restaurant.")
            calculated_total += menu_item.price * order_item.quantity

        calculated_total = calculated_total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        if calculated_total != order.total_amount:
            raise ValueError("Order total does not match its order items.")


def generate_sql(
    restaurants: list[Restaurant],
    customers: list[Customer],
    employees: list[Employee],
    dining_tables: list[DiningTable],
    menu_items: list[MenuItem],
    reservations: list[Reservation],
    orders: list[Order],
    order_items: list[OrderItem],
) -> str:
    sections: list[str] = [
        """USE RestaurantReservationDB;
GO

SET NOCOUNT ON;
SET XACT_ABORT ON;
GO

/*
    Generated by generate_seed_data.py.
    The cleanup section makes this script safely rerunnable on the project database.
*/

BEGIN TRY
    BEGIN TRANSACTION;

    DELETE FROM OrderItems;
    DELETE FROM Orders;
    DELETE FROM Reservations;
    DELETE FROM MenuItems;
    DELETE FROM Tables;
    DELETE FROM Employees;
    DELETE FROM Customers;
    DELETE FROM Restaurants;

    DBCC CHECKIDENT ('OrderItems', RESEED, 0);
    DBCC CHECKIDENT ('Orders', RESEED, 0);
    DBCC CHECKIDENT ('Reservations', RESEED, 0);
    DBCC CHECKIDENT ('MenuItems', RESEED, 0);
    DBCC CHECKIDENT ('Tables', RESEED, 0);
    DBCC CHECKIDENT ('Employees', RESEED, 0);
    DBCC CHECKIDENT ('Customers', RESEED, 0);
    DBCC CHECKIDENT ('Restaurants', RESEED, 0);
"""
    ]

    restaurant_rows = [
        (
            sql_string(r.name),
            sql_string(r.address),
            sql_string(r.phone_number),
            sql_string(r.opening_hours),
        )
        for r in restaurants
    ]
    sections.append(build_insert(
        "Restaurants",
        ["Name", "Address", "PhoneNumber", "OpeningHours"],
        restaurant_rows,
    ))

    customer_rows = [
        (
            sql_string(c.first_name),
            sql_string(c.last_name),
            sql_string(c.email),
            sql_string(c.phone_number),
        )
        for c in customers
    ]
    sections.append(build_insert(
        "Customers",
        ["FirstName", "LastName", "Email", "PhoneNumber"],
        customer_rows,
    ))

    employee_rows = [
        (
            str(e.restaurant_id),
            sql_string(e.first_name),
            sql_string(e.last_name),
            sql_string(e.position),
        )
        for e in employees
    ]
    sections.append(build_insert(
        "Employees",
        ["RestaurantId", "FirstName", "LastName", "Position"],
        employee_rows,
    ))

    table_rows = [
        (str(t.restaurant_id), str(t.capacity))
        for t in dining_tables
    ]
    sections.append(build_insert(
        "Tables",
        ["RestaurantId", "Capacity"],
        table_rows,
    ))

    menu_rows = [
        (
            str(m.restaurant_id),
            sql_string(m.name),
            sql_string(m.description),
            sql_decimal(m.price),
        )
        for m in menu_items
    ]
    sections.append(build_insert(
        "MenuItems",
        ["RestaurantId", "Name", "Description", "Price"],
        menu_rows,
    ))

    reservation_rows = [
        (
            str(r.customer_id),
            str(r.restaurant_id),
            str(r.table_id),
            sql_datetime(r.reservation_date),
            str(r.party_size),
        )
        for r in reservations
    ]
    sections.append(build_insert(
        "Reservations",
        ["CustomerId", "RestaurantId", "TableId", "ReservationDate", "PartySize"],
        reservation_rows,
    ))

    order_rows = [
        (
            str(o.reservation_id),
            str(o.employee_id),
            sql_datetime(o.order_date),
            sql_decimal(o.total_amount),
        )
        for o in orders
    ]
    sections.append(build_insert(
        "Orders",
        ["ReservationId", "EmployeeId", "OrderDate", "TotalAmount"],
        order_rows,
    ))

    order_item_rows = [
        (
            str(oi.order_id),
            str(oi.item_id),
            str(oi.quantity),
        )
        for oi in order_items
    ]
    sections.append(build_insert(
        "OrderItems",
        ["OrderId", "ItemId", "Quantity"],
        order_item_rows,
    ))

    sections.append(
        """
    IF (SELECT COUNT(*) FROM Restaurants) <> 50
        THROW 51000, 'Expected 50 Restaurants.', 1;
    IF (SELECT COUNT(*) FROM MenuItems) <> 1000
        THROW 51000, 'Expected 1000 MenuItems.', 1;
    IF (SELECT COUNT(*) FROM OrderItems) <> 1500
        THROW 51000, 'Expected 1500 OrderItems.', 1;
    IF (SELECT COUNT(*) FROM Orders) <> 500
        THROW 51000, 'Expected 500 Orders.', 1;
    IF (SELECT COUNT(*) FROM Employees) <> 100
        THROW 51000, 'Expected 100 Employees.', 1;
    IF (SELECT COUNT(*) FROM Reservations) <> 500
        THROW 51000, 'Expected 500 Reservations.', 1;
    IF (SELECT COUNT(*) FROM Customers) <> 400
        THROW 51000, 'Expected 400 Customers.', 1;
    IF (SELECT COUNT(*) FROM Tables) <> 100
        THROW 51000, 'Expected 100 Tables.', 1;

    IF EXISTS
    (
        SELECT 1
        FROM Reservations AS r
        INNER JOIN Tables AS t
            ON t.TableId = r.TableId
        WHERE t.RestaurantId <> r.RestaurantId
           OR r.PartySize > t.Capacity
    )
        THROW 51000, 'Invalid reservation/table relationship.', 1;

    IF EXISTS
    (
        SELECT 1
        FROM Orders AS o
        INNER JOIN Reservations AS r
            ON r.ReservationId = o.ReservationId
        INNER JOIN Employees AS e
            ON e.EmployeeId = o.EmployeeId
        WHERE e.RestaurantId <> r.RestaurantId
    )
        THROW 51000, 'An order uses an employee from another restaurant.', 1;

    IF EXISTS
    (
        SELECT 1
        FROM OrderItems AS oi
        INNER JOIN Orders AS o
            ON o.OrderId = oi.OrderId
        INNER JOIN Reservations AS r
            ON r.ReservationId = o.ReservationId
        INNER JOIN MenuItems AS mi
            ON mi.ItemId = oi.ItemId
        WHERE mi.RestaurantId <> r.RestaurantId
    )
        THROW 51000, 'An order item belongs to another restaurant.', 1;

    IF EXISTS
    (
        SELECT o.OrderId
        FROM Orders AS o
        INNER JOIN OrderItems AS oi
            ON oi.OrderId = o.OrderId
        INNER JOIN MenuItems AS mi
            ON mi.ItemId = oi.ItemId
        GROUP BY o.OrderId, o.TotalAmount
        HAVING o.TotalAmount <> SUM(mi.Price * oi.Quantity)
    )
        THROW 51000, 'An order total does not match its items.', 1;

    COMMIT TRANSACTION;
END TRY
BEGIN CATCH
    IF @@TRANCOUNT > 0
        ROLLBACK TRANSACTION;

    THROW;
END CATCH;
GO

SELECT N'Restaurants' AS TableName, COUNT(*) AS RecordCount FROM Restaurants
UNION ALL
SELECT N'MenuItems', COUNT(*) FROM MenuItems
UNION ALL
SELECT N'OrderItems', COUNT(*) FROM OrderItems
UNION ALL
SELECT N'Orders', COUNT(*) FROM Orders
UNION ALL
SELECT N'Employees', COUNT(*) FROM Employees
UNION ALL
SELECT N'Reservations', COUNT(*) FROM Reservations
UNION ALL
SELECT N'Customers', COUNT(*) FROM Customers
UNION ALL
SELECT N'Tables', COUNT(*) FROM Tables;
GO
"""
    )

    # GO is not legal inside an active SQL transaction batch. Remove batch separators
    # from generated INSERT sections while preserving the final separators outside it.
    sql = "\n\n".join(sections)
    transaction_start = sql.index("BEGIN TRY")
    transaction_end = sql.index("    COMMIT TRANSACTION;")
    before = sql[:transaction_start]
    transaction_body = sql[transaction_start:transaction_end].replace("\nGO", "")
    after = sql[transaction_end:]
    return before + transaction_body + after


def main() -> None:
    rng = random.Random(RANDOM_SEED)

    restaurants = generate_restaurants()
    customers = generate_customers()
    employees = generate_employees()
    dining_tables = generate_tables()
    menu_items = generate_menu_items()
    reservations = generate_reservations(rng, dining_tables)
    orders, order_items = generate_orders_and_items(
        rng,
        reservations,
        employees,
        menu_items,
    )

    validate_data(
        restaurants,
        customers,
        employees,
        dining_tables,
        menu_items,
        reservations,
        orders,
        order_items,
    )

    sql = generate_sql(
        restaurants,
        customers,
        employees,
        dining_tables,
        menu_items,
        reservations,
        orders,
        order_items,
    )
    OUTPUT_FILE.write_text(sql, encoding="utf-8")

    print(f"Created: {OUTPUT_FILE}")
    for table_name, count in COUNTS.items():
        print(f"{table_name}: {count}")


if __name__ == "__main__":
    main()