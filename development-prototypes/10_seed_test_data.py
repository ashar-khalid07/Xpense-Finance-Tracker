"""Representative test data for exercising totals, filters and charts."""
from datetime import date
from decimal import Decimal

TEST_EXPENSES = [
    {"description": "Weekly groceries", "amount": Decimal("62.40"), "category": "Food", "date": date(2026, 10, 1)},
    {"description": "Train ticket", "amount": Decimal("14.80"), "category": "Transport", "date": date(2026, 10, 1)},
    {"description": "Coffee", "amount": Decimal("4.25"), "category": "Food", "date": date(2026, 10, 2)},
    {"description": "October rent", "amount": Decimal("850.00"), "category": "Rent", "date": date(2026, 10, 3)},
    {"description": "Electricity", "amount": Decimal("74.30"), "category": "Utilities", "date": date(2026, 10, 4)},
    {"description": "Prescription", "amount": Decimal("9.90"), "category": "Health", "date": date(2026, 10, 5)},
    {"description": "Dinner", "amount": Decimal("31.60"), "category": "Food", "date": date(2026, 10, 5)},
]

# Useful expected results:
# Food total = 98.25
# 2026-10-01 daily total = 77.20
# Overall total = 1047.25
