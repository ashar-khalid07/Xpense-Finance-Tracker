"""Prototype 1: understand the data shape before introducing a database.

This deliberately uses a list of dictionaries. Data disappears when the
program restarts, but it is useful for proving the data model and algorithms.
"""
from decimal import Decimal

expenses = [
    {
        "id": 1,
        "description": "Groceries",
        "amount": Decimal("42.80"),
        "category": "Food",
        "date": "2026-10-01",
    },
    {
        "id": 2,
        "description": "Bus pass",
        "amount": Decimal("18.50"),
        "category": "Transport",
        "date": "2026-10-02",
    },
]

total = sum((item["amount"] for item in expenses), Decimal("0.00"))
food_expenses = [item for item in expenses if item["category"] == "Food"]

print("Total:", total)
print("Food expenses:", food_expenses)
